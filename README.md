# Anobi Marketing Portal

This repository contains a small Flask web application for marketers. The app
includes a Materialize styled UI with login and registration, an about page,
a dashboard showing sample marketing news and posting times and a basic AI chat
interface implemented with simple rules. User accounts are stored in Firebase
Firestore so you will need a service account to run the app.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```

### Firebase setup

Create a Firebase project and download a service account JSON file. Set the
`FIREBASE_CRED` environment variable to the path of this file before starting
the server. The app uses Firestore to store user credentials.

The server will start on `http://127.0.0.1:5000/`.

Once running you can visit `/about` to read more about the portal.
