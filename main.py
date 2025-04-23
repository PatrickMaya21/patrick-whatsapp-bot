from flask import Flask, request, jsonify
import requests
import openai
import os

app = Flask(__name__)

# OPENAI 1.x: usando chave do tipo sk-proj
openai.api_key = "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"

# Z-API config
ZAPI_INSTANCE = "3E01E904D77EE0E2921F8E66062CE0C1"
ZAPI_TOKEN = "948E3B5FF7F285EC974430DC"
ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"

PROMPT_BASE = """
Você é o Patrick Maya, corretor de imóveis de alto padrão em Balneário Camboriú. Responda como se fosse ele, com um tom simpático, direto e com autoridade. Utilize expressões como "meu caro", "vamos nessa", "te mostro agora mesmo". Seja cordial, mas ágil. Quando apropriado, convide o cliente para agendar uma visita ou pedir mais opções de imóveis.
"""

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print("📥 Dados recebidos:", data)

        message = data.get("text", {}).get("message")
        phone = data.get("phone")

        if not message or not phone:
            print("❌ Campos ausentes.")
            return jsonify({"erro": "Faltam dados"}), 400

        # novo formato para ChatCompletion na OpenAI >= 1.x
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT_BASE},
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message.content.strip()

        payload = {
            "phone": phone,
            "message": reply
        }

        headers = {
            "Content-Type": "application/json",
            "Client-Token": ZAPI_TOKEN
        }

        zap_response = requests.post(ZAPI_URL, json=payload, headers=headers)
        print("📤 Resposta enviada:", zap_response.status_code, zap_response.text)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        import traceback
        print("❌ ERRO DETALHADO:")
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
