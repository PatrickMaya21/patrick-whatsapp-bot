from flask import Flask, request, jsonify
import requests
import openai
import os

app = Flask(__name__)

# Configure sua chave da API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# URL da Z-API
ZAPI_URL = "https://api.z-api.io/instances/3E01E904D77EE0E2921F8E66062CE0C1/token/948E3B5FF7F285EC974430DC/send-text"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 Dados recebidos:", data)

    # Verifique se os campos necessários estão presentes
    if not data or "text" not in data or "message" not in data["text"] or "phone" not in data:
        print("❌ Dados incompletos no payload.")
        return jsonify({"status": "erro", "mensagem": "Dados incompletos"}), 400

    message = data["text"]["message"]
    phone = data["phone"]

    # Gere a resposta usando o OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Erro ao gerar resposta do OpenAI:", e)
        reply = "Desculpe, ocorreu um erro ao processar sua mensagem."

    # Envie a resposta de volta via Z-API
    payload = {
        "phone": phone,
        "message": reply
    }
    try:
        zapi_response = requests.post(ZAPI_URL, json=payload)
        print("📤 Resposta enviada:", zapi_response.status_code, zapi_response.text)
    except Exception as e:
        print("❌ Erro ao enviar resposta via Z-API:", e)

    return jsonify({"status": "sucesso"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
