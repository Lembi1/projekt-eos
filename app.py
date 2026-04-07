from flask import Flask, request, jsonify, render_template
import requests
import datetime
import os

app = Flask(__name__)

# Domovská stránka s HTML rozhraním
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ping', methods=['GET'])
def ping():
    return "pong" # Endpoint GET/ping dle zadání [cite: 15, 23]

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "cas": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "autor": "Tvoje Jmeno", # Sem si doplň jméno kvůli bodům [cite: 23]
        "projekt": "LoL Build Helper"
    })

@app.route('/ai', methods=['POST'])
def ai():
    data = request.json
    user_prompt = data.get("prompt", "")
    
    # Konfigurace pro Ollama/LM Studio dle zadání [cite: 17, 28]
    ollama_data = {
        "model": "gemma2:2b",
        "prompt": f"Jsi expert na League of Legends. Odpověz jednou krátkou větou na: {user_prompt}",
        "stream": False
    }
    
    try:
        # Používáme host.docker.internal pro přístup z kontejneru na hostitele [cite: 17, 25]
        response = requests.post("http://host.docker.internal:11434/api/generate", json=ollama_data)
        return jsonify({"odpoved": response.json().get("response")})
    except Exception as e:
        return jsonify({"chyba": "AI nedostupné: " + str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' zajistí, že aplikace je VEŘEJNÁ v rámci sítě 
    # port=8081 je nestandardní port vyžadovaný zadáním [cite: 8, 16]
    app.run(host='0.0.0.0', port=8081)