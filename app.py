from flask import Flask, request, render_template
import os
import requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Load Groq API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    email = None

    if request.method == 'POST':
        if request.form.get('action') == 'reset':
            return render_template("index.html", email=None)

        sender = request.form['sender']
        receiver = request.form['receiver']
        topic = request.form['topic']
        tone = request.form['tone']
        wordcount = request.form['wordcount']

        prompt = f"Write a {tone} email from {sender} to {receiver} about {topic} in about {wordcount} words."

        try:
            # Groq API call
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mixtral-8x7b-32768",  # You can also try "llama3-8b-8192"
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }

            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            email = response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            email = f"Error: {str(e)}"

    return render_template("index.html", email=email)

if __name__ == '__main__':
    app.run(debug=True)