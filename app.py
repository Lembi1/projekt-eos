from flask import Flask, request, jsonify, render_template

import requests

import datetime

import os

import urllib3



# ✅ Vypnutí varování o SSL (nezbytné pro váš server)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



app = Flask(__name__)



# ✅ Načtení konfigurace z ENV (aby to fungovalo na serveru i lokálně)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://kurim.ithope.eu/v1")



@app.route('/')

def home():

    return render_template('index.html')



@app.route('/ping', methods=['GET'])

def ping():

    return "pong"



@app.route('/status', methods=['GET'])

def status():

    return jsonify({

        "cas": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "autor": "Tvoje Jmeno", # Tady si kamarád dopíše jméno

        "projekt": "LoL Build Helper"

    })



@app.route('/ai', methods=['POST'])

def ai():

    data = request.json

    user_prompt = data.get("prompt", "")

    

    # ✅ Oprava URL na standardní OpenAI chat endpoint

    clean_url = OPENAI_BASE_URL.rstrip('/')

    target_url = f"{clean_url}/chat/completions"



    # ✅ Oprava struktury dat pro OpenAI standard

    payload = {

        "model": "gemma3:27b",

        "messages": [

            {

                "role": "system", 

                "content": "Jsi expert na League of Legends. Odpovídáš stručně jednou větou v češtině."

            },

            {

                "role": "user", 

                "content": user_prompt

            }

        ],

        "stream": False

    }



    headers = {

        "Authorization": f"Bearer {OPENAI_API_KEY}",

        "Content-Type": "application/json"

    }

    

    try:

        # ✅ Přidáno verify=False a správné parametry

        response = requests.post(

            target_url, 

            json=payload, 

            headers=headers, 

            timeout=20, 

            verify=False

        )

        

        if response.status_code == 200:

            # ✅ Oprava parsování odpovědi (choices[0]...)

            ai_content = response.json()['choices'][0]['message']['content']

            return jsonify({"odpoved": ai_content})

        else:

            return jsonify({"chyba": f"Server vrátil chybu {response.status_code}"}), response.status_code



    except Exception as e:

        return jsonify({"chyba": "AI nedostupné: " + str(e)}), 500



if __name__ == '__main__':

    # ✅ Port 8081 ponechán dle zadání

    port = int(os.environ.get("PORT", 8081))

    app.run(host='0.0.0.0', port=port)
