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
    data = request.get_json()
    message = data.get("message", "")
    phone = data.get("phone", "")

    if not message or not phone:
        return jsonify({"error": "Mensagem ou telefone ausente."}), 400

    full_prompt = PROMPT_BASE + f"\n\nMensagem do cliente: {message}\nResposta:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        temperature=0.8,
        max_tokens=200
    )

    reply = response.choices[0].text.strip()

    payload = {
        "phone": phone,
        "message": reply
    }
    zap_response = requests.post(ZAPI_URL, json=payload)

    if zap_response.status_code == 200:
        return jsonify({"status": "mensagem enviada", "resposta": reply})
    else:
        return jsonify({"erro": "falha ao enviar mensagem via Z-API"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
