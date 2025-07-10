import os
from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize Firebase using a service account json file specified via the
# FIREBASE_CRED environment variable.  This allows the app to store and
# retrieve user credentials in Firestore.
cred_path = os.environ.get("FIREBASE_CRED", "firebase_service_account.json")
if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    DB = firestore.client()
else:
    DB = None


# Fake news and posting schedule data
NEWS = [
    "Social media marketing trends for 2025",
    "10 tips to boost engagement",
    "New algorithm changes on major platforms"
]
POST_TIMES = [
    "Best time to post on Twitter: 12pm-3pm",
    "Best time to post on Instagram: 4pm-6pm"
]

class SimpleAgent:
    def respond(self, message: str) -> str:
        message_lower = message.lower()
        if 'followers' in message_lower:
            return "Focus on quality content and consistent posting to grow followers."
        if 'content' in message_lower:
            return "Engage with your audience by asking questions and sharing insights."
        return "That's interesting! Tell me more about your marketing goals."

agent = SimpleAgent()


def get_user(username: str):
    """Fetch a user document from Firestore."""
    if DB:
        doc = DB.collection("users").document(username).get()
        if doc.exists:
            return doc.to_dict()
    return None


def create_user(username: str, password: str) -> bool:
    """Create a new user. Returns True on success, False if user exists."""
    if not DB:
        return False
    if get_user(username):
        return False
    DB.collection("users").document(username).set({"password": password})
    return True

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user and user.get("password") == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Allow new users to create an account."""
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if create_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        message = 'User already exists'
    return render_template('register.html', message=message)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', news=NEWS, times=POST_TIMES)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    response = None
    if request.method == 'POST':
        user_msg = request.form.get('message', '')
        response = agent.respond(user_msg)
    return render_template('chat.html', response=response)


@app.route('/about')
def about():
    """Render the about page with information about the portal."""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
