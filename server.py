from flask import Flask, request, jsonify, send_from_directory
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Route pour l'API chat
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    try:
        completion = client.chat.completions.create(
            model="llama3-7b-4096",  # <-- modèle supporté
            messages=[
                {"role": "system", "content": "Tu es un assistant médical d'accueil. Tu discutes poliment, tu rediriges les patients vers le bon médecin si nécessaire."},
                {"role": "user", "content": message}
            ]
        )
        answer = completion.choices[0].message.content
        return jsonify({"reply": answer})

    except Exception as e:
        return jsonify({"reply": f"Erreur serveur : {str(e)}"}), 500

# Route pour servir le front HTML
@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
