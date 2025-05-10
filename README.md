# XYZ Real Estate Chatbot

A sophisticated AI-powered real estate assistant that combines natural language processing with CRM integration to provide intelligent property information and lead management.

## Overview

XYZ Real Estate Chatbot is an intelligent conversational agent designed to streamline real estate inquiries and lead management. Built with Python and Flask, it leverages advanced AI technologies to provide accurate property information while automatically qualifying and managing leads through HubSpot CRM integration.

🔗 **Live Demo**: [Try the Chatbot](https://xyz-real-state-chatbot-2.onrender.com)

## Key Features

- 🤖 **AI-Powered Conversations**: Intelligent responses to real estate queries using advanced LLM technology
- 📊 **Automated Lead Scoring**: Real-time evaluation and qualification of potential leads
- 🔄 **HubSpot CRM Integration**: Seamless lead management and tracking
- 🔍 **Smart Context Search**: FAISS-powered vector search for accurate information retrieval
- 📱 **Responsive Interface**: Clean, user-friendly chat interface
- 📈 **Real-time Analytics**: Instant lead qualification and status updates

## Technical Highlights

- **Backend Framework**: Flask (Python)
- **AI Components**: 
  - Sentence Transformers for semantic understanding
  - FAISS for efficient vector similarity search
  - Groq LLM for natural language processing
- **CRM Integration**: HubSpot API
- **Deployment**: Render cloud platform

## Core Functionalities

1. **Intelligent Chat Processing**
   - Natural language understanding
   - Context-aware responses
   - Real estate domain expertise

2. **Lead Management**
   - Automated lead scoring
   - Lead qualification
   - CRM synchronization
   - Contact management

3. **Real Estate Information**
   - Property details
   - Market insights
   - Buying/Selling guidance
   - Location information

## Use Cases

- Property inquiries
- Real estate market questions
- Buying/Selling guidance
- Investment advice
- Property comparisons
- Neighborhood information

## Benefits

- 24/7 Availability
- Instant response to inquiries
- Automated lead qualification
- Reduced manual CRM entry
- Consistent user experience
- Scalable customer support

## Deployment (Render)

1. **Set Environment Variables** in Render dashboard:
   - `HUBSPOT_API_KEY`
   - `GROQ_API_KEY`
   - `FLASK_SECRET_KEY`
   - (Any other required keys)

2. **Add a Build Command** (if needed):
   ```sh
   pip install -r requirements.txt
   ```

3. **Set the Start Command**:
   ```sh
   gunicorn app:app
   ```

4. **Port Configuration**: The app will use the `PORT` environment variable automatically.

5. **Security**: Do not commit your `.env` file or any secrets to the repository. All secrets should be set as environment variables in Render.

6. **Production Notes**:
   - Flask debug mode is OFF in production.
   - For rate limiting, consider using a Redis backend for Flask-Limiter in production.

7. **Optional: render.yaml**
   You can add a `render.yaml` for infrastructure-as-code deployment (see Render docs).
