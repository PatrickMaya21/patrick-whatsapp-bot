from flask import Flask, request, jsonify
import requests
import openai
import os

app = Flask(__name__)

ZAPI_URL = "https://api.z-api.io/instances/3E01E904D77EE0E2921F8E66062CE0C1/token/948E3B5FF7F285EC974430DC/send-text"
openai.api_key = "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"

PROMPT_BASE = """
Você é o Patrick Maya, corretor de imóveis de alto padrão em Balneário Camboriú. Responda como se fosse ele, com um tom simpático, direto e com autoridade. Utilize expressões como "meu caro", "vamos nessa", "te mostro agora mesmo". Seja cordial, mas ágil. Quando apropriado, convide o cliente para agendar uma visita ou pedir mais opções de imóveis.
"""

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True)
    
    print("🔹 JSON BRUTO RECEBIDO DA Z-API:")
    print(data)

    return jsonify({"ok": True}), 200



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
