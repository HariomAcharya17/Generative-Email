from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    email = None

    if request.method == 'POST':
        if request.form.get('action') == 'reset':
            # Just reload the form, clearing everything
            return render_template("index.html", email=None)

        sender = request.form['sender']
        receiver = request.form['receiver']
        topic = request.form['topic']
        tone = request.form['tone']
        wordcount = request.form['wordcount']

        prompt = f"Write a {tone} email from {sender} to {receiver} about {topic} in about {wordcount} words."

        try:
            result = subprocess.run(
                ['ollama', 'run', 'mistral'],
                input=prompt.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            email = result.stdout.decode('utf-8') or result.stderr.decode('utf-8')
        except Exception as e:
            email = f"Error: {str(e)}"

    return render_template("index.html", email=email)

if __name__ == '__main__':
    app.run(debug=True)