from flask import Flask, request, render_template
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env (local testing)
load_dotenv()

app = Flask(__name__)

# Get Groq API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    email = None
    error = None

    if request.method == 'POST':
        if request.form.get('action') == 'reset':
            return render_template("index.html", email=None)

        sender = request.form['sender']
        receiver = request.form['receiver']
        topic = request.form['topic']
        tone = request.form['tone']
        wordcount = request.form['wordcount']

        # Prepare prompt
        prompt = f"Write a {tone} email from {sender} to {receiver} about {topic} in about {wordcount} words."

        try:
            # Prepare request
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "llama3-8b-8192",  # More stable for first-time users
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )

            # If request failed
            if response.status_code != 200:
                error = f"Groq API error {response.status_code}: {response.text}"
                email = None
            else:
                email = response.json()['choices'][0]['message']['content']

        except Exception as e:
            email = None
            error = f"Exception: {str(e)}"

    return render_template("index.html", email=email, error=error)

if __name__ == '__main__':
    app.run(debug=True)