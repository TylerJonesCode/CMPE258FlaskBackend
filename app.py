from flask import Flask, request, jsonify
import requests
import tempfile
from llm import LLMRequestHandler, speechToText



app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Render!"

@app.route("/speech", methods=["POST"])
def speech():
    data = request.get_json()
    audioUrl = data.get("audioUrl")
    audioConfig = data.get("audioConfig")

    if not audioUrl or not audioConfig:
        response = jsonify({"error": "no audioUrl or config"})
        response.status_code = 400
        return response

    try:
        audio = requests.get(audioUrl)
        text = None
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
            tmp.write(response.content)
            tmp.flush()
            text = speechToText(tmp, audioConfig)

        if text is None:
            response = jsonify({"error": "whisper speech translation failed"})
            response.status_code = 400
            return response
        
        print(f"Model transcription complete: {text}")
        
        response = jsonify({"content": text})
        response.status_code = 200
        return response

    except Exception as e:
        response = jsonify({"error": str(e)})
        response.status_code = 500
        return response

@app.route("/model", methods=["POST"])
def model():
    return jsonify({"text": "hi"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)