from flask import Flask, request, jsonify, render_template
import requests
import datetime
import os
import urllib3
import sqlite3

# Vypnutí varování o SSL pro školní server
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Nastavení databáze
DB_PATH = 'historie.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chaty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cas TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                dotaz TEXT,
                odpoved TEXT
            )
        ''')

init_db()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://kurim.ithope.eu/v1")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/historie', methods=['GET'])
def historie():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM chaty ORDER BY cas DESC")
            rows = cursor.fetchall()
            return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({"chyba": str(e)}), 500

@app.route('/ai', methods=['POST'])
def ai():
    data = request.json
    user_prompt = data.get("prompt", "")
    clean_url = OPENAI_BASE_URL.rstrip('/')
    target_url = f"{clean_url}/chat/completions"

    payload = {
        "model": "gemma3:27b",
        "messages": [
            {"role": "system", "content": "Jsi expert na League of Legends. Odpovídáš stručně jednou větou v češtině."},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(target_url, json=payload, headers=headers, timeout=20, verify=False)
        if response.status_code == 200:
            ai_content = response.json()['choices'][0]['message']['content']
            
            # Zápis do databáze
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO chaty (dotaz, odpoved) VALUES (?, ?)", (user_prompt, ai_content))

            return jsonify({"odpoved": ai_content})
        return jsonify({"chyba": "Chyba AI"}), response.status_code
    except Exception as e:
        return jsonify({"chyba": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8081))
    app.run(host='0.0.0.0', port=port)
