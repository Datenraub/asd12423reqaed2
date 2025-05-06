
from flask import Flask, render_template, request, redirect, url_for, flash
import json, os

app = Flask(__name__)
app.secret_key = 'dein_secret_key'

TOKENS_FILE = 'tokens.json'
SPRUCH_FILE = 'sprüche.json'

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    tokens = load_json(TOKENS_FILE)
    sprueche = load_json(SPRUCH_FILE)
    return render_template('dashboard.html', tokens=tokens, sprueche=sprueche)

@app.route('/add_token', methods=['POST'])
def add_token():
    token = request.form['token'].strip()
    tokens = load_json(TOKENS_FILE)
    if token and token not in tokens:
        tokens.append(token)
        save_json(TOKENS_FILE, tokens)
        flash("Token hinzugefügt.")
    return redirect(url_for('index'))

@app.route('/add_spruch', methods=['POST'])
def add_spruch():
    spruch = request.form['spruch'].strip()
    sprueche = load_json(SPRUCH_FILE)
    if spruch and spruch not in sprueche:
        sprueche.append(spruch)
        save_json(SPRUCH_FILE, sprueche)
        flash("Spruch hinzugefügt.")
    return redirect(url_for('index'))

@app.route('/spam', methods=['POST'])
def spam():
    channel = request.form['channel']
    message = request.form['message']
    # Hier kommt dein echter Spam-Code rein
    flash(f"Spam gestartet in Channel {channel} mit Message: {message}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
