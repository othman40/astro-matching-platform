# Astro Matching Platform MVP

A simple astrology matching platform focused on core functionality.

## Tech Stack
- **Frontend**: Flutter + Dart
- **Backend**: Python (FastAPI)
- **Database**: SQLite (for MVP)
- **API Provider**: Prokerala Astrology API

## Core Flow
1. User enters birth data (name, gender, birth date/time, birth city)
2. Backend sends data to Prokerala Astrology API
3. API returns natal chart data (planetary positions, ascendant, houses)
4. Backend saves astrology data in user profile
5. App displays profile with saved natal data
6. Search and matching based on custom compatibility algorithm

## Project Structure
```
astro_matching_platform/
├── backend/          # Python FastAPI backend
├── frontend/         # Flutter app
└── README.md         # This file
```

## Setup Instructions

### Backend
1. Navigate to `backend/` directory
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `uvicorn main:app --reload`

### Frontend
1. Navigate to `frontend/` directory
2. Run: `flutter pub get`
3. Run: `flutter run`

## API Keys
You'll need to get an API key from Prokerala Astrology API and set it in the backend environment variables.
