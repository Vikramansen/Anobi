from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Simple in-memory user store
USERS = {'marketing_dude': 'password'}

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

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

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
