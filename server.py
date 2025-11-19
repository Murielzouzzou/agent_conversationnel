from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Tu es un assistant médical d'accueil. Tu discutes poliment, tu rediriges les patients vers le bon médecin si nécessaire."},
            {"role": "user", "content": message}
        ]
    )

    answer = completion.choices[0].message.content
    return jsonify({"reply": answer})

@app.route("/")
def home():
    return "Server is up"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

