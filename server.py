from flask import Flask, request, jsonify
from llm_brain import ask_llm

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    reply = ask_llm(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(port=5000, debug=True)

