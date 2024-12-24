# SafeHaven: Natural Calamity Alert System

A real-time disaster alert and management system built with Django that helps people during natural calamities by providing location-based alerts, distress signals, and shelter information.

## Features

- **One-Click Distress Signal**: Automatically captures user's geolocation when activated
- **AI-Powered Verification**: Uses Groq model to verify legitimacy of distress signals
- **Real-time Updates**: Implements WebSocket connections using Django Channels for instant alerts
- **Interactive Map Interface**: Displays affected areas and nearby shelters using Google Maps API
- **Emergency Broadcast**: Automated email notifications to all registered users
- **Shelter Locator**: Shows list of nearby safe shelters with directions
- **Distress List**: Public registry of people requiring assistance with their locations

## Tech Stack

### Backend
- Django - Web framework
- Daphne - ASGI server
- Redis - Channel layer for WebSocket connections
- Groq - AI model integration for verification
- Django Channels - WebSocket implementation

### Frontend
- HTML5
- CSS3
- JavaScript
- Google Maps API

## Prerequisites

- Python 3.8+
- Redis Server
- Google Maps API key
- Groq API key

## Installation

1. Clone the repository
```bash
git clone https://github.com/sathwikshetty33/safehaven.git
cd natural-calamity-alert
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```


5. Run Redis Server
```bash
redis-server --port 6380
```

6. Apply database migrations
```bash
python manage.py migrate
```

7. Start the development server
```bash
py manage.py runserver
```

## Usage

1. Register/Login to the platform
2. Enable location services in your browser
3. In case of emergency:
   - Click the alert button
   - Your location will be automatically captured
   - Select the type of natural calamity
   - Submit the alert




