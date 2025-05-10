import requests
import os
from dotenv import load_dotenv
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# HubSpot API configuration
HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
if not HUBSPOT_API_KEY:
    raise ValueError("HUBSPOT_API_KEY environment variable not set")
HUBSPOT_BASE_URL = "https://api.hubapi.com"

def validate_api_key():
    """Validate HubSpot API key by making a test request."""
    test_url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(test_url, headers=headers)
        response.raise_for_status()
        logger.info("HubSpot API key validated successfully")
        return True
    except Exception as e:
        logger.error(f"HubSpot API key validation failed: {str(e)}")
        return False

# Validate API key on module load
if not validate_api_key():
    logger.error("Invalid HubSpot API key")
    raise ValueError("Invalid HubSpot API key")

def create_or_update_contact(email, name, budget, lead_type, lead_score, qualification, chat_history, user_type):
    """Create or update a contact in HubSpot CRM."""
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Validate and format properties
    try:
        # Validate email format
        if not email or '@' not in email:
            logger.error(f"Invalid email format: {email}")
            return 400, {"error": "Invalid email format"}
            
        # Format budget as string and ensure it's numeric
        budget_str = str(budget).replace('$', '').replace(',', '')
        if budget_str.isdigit():
            budget_formatted = budget_str
        else:
            budget_formatted = "0"
            
        # Format lead score as integer
        lead_score_int = int(float(str(lead_score)))
        
        # Ensure chat history doesn't exceed limit
        chat_history_truncated = chat_history[:5000] if chat_history else ""
        
        # Format properties according to HubSpot's API requirements
        properties = {
            "properties": {
                "email": email.strip(),
                "firstname": name.strip() if name else "Unknown",
                "budget": budget_formatted,
                "lead_type": lead_type.strip() if lead_type else "Unknown",
                "lead_score": str(lead_score_int),
                "lead_qualification": qualification.strip() if qualification else "Unknown",
                "chat_history": chat_history_truncated,
                "user_type": user_type.strip() if user_type else "User"
            }
        }
        
        logger.info(f"Formatted properties: {json.dumps(properties, indent=2)}")
        
    except Exception as e:
        logger.error(f"Error formatting properties: {str(e)}")
        return 500, {"error": f"Property formatting error: {str(e)}"}
    
    search_url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/search"
    search_payload = {
        "filterGroups": [{"filters": [{"propertyName": "email", "operator": "EQ", "value": email}]}]
    }
    
    try:
        # First, search for existing contact
        logger.info(f"Searching for contact with email: {email}")
        search_response = requests.post(search_url, headers=headers, json=search_payload)
        search_response.raise_for_status()
        results = search_response.json().get("results", [])
        
        if results:
            # Update existing contact
            contact_id = results[0]["id"]
            update_url = f"{url}/{contact_id}"
            logger.info(f"Updating existing contact: {contact_id}")
            response = requests.patch(update_url, headers=headers, json=properties)
            response.raise_for_status()
            logger.info("CRM update successful")
            return response.status_code, response.json()
        else:
            # Create new contact
            logger.info("Creating new contact")
            response = requests.post(url, headers=headers, json=properties)
            response.raise_for_status()
            logger.info("CRM update successful")
            return response.status_code, response.json()
            
    except requests.RequestException as e:
        logger.error(f"HubSpot API Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response text: {e.response.text}")
            logger.error(f"Request URL: {e.response.request.url}")
            logger.error(f"Request headers: {e.response.request.headers}")
            logger.error(f"Request body: {e.response.request.body}")
        return 500, {"error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 500, {"error": str(e)}