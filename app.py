from flask import Flask, request, jsonify
import requests
import tempfile
import logging
from llm import LLMRequestHandler, speechToText
import base64

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
)

@app.route('/')
def home():
    logging.info("Home Route Accessed")
    return "Hello, Render!"

@app.route("/speech", methods=["POST"])
def speech():
    logging.info("Speech Detection Accessed")
    data = request.get_json()

    if data is None:
        logging.info("????")

    audioUrl = data.get("audioUrl")
    audioConfig = data.get("config")

    if not audioUrl:
        logging.info("no audioUrl")
    
    if not audioConfig:
        logging.info("no audio Config")

    if not audioUrl or not audioConfig:
        response = jsonify({"error": "no audioUrl or config"})
        response.status_code = 400
        return response

    logging.info("uri and config found")
    

    try:
        logging.info("beginning audio processing")
        
        #logging.info(f"audio url: {audioUrl}")
        #logging.info(f"Length of audio_base64: {len(audioUrl)}")
        
        audio_bytes = base64.b64decode(audioUrl)

        text = None
         
        logging.info("audio is inputted into the model")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
            logging.info("temp file made")
            tmp.write(audio_bytes)
            tmp.flush()
            tmp.seek(0)
            logging.info("audio written to temp file")
            text = speechToText(tmp.name)

        logging.info("model processing is completed")

        if text is None:
            response = jsonify({"error": "whisper speech translation failed"})
            response.status_code = 400
            return response
        
        logging.info(f"Model transcription complete: {text}")
        
        response = jsonify({"content": text})
        response.status_code = 200
        return response

    except Exception as e:
        response = jsonify({"error": str(e)})
        response.status_code = 500
        return response

@app.route("/model", methods=["POST"])
def model():
    logging.info("Speech Detection Accessed")
    data = request.get_json()

    if data is None:
        logging.info("????")

    audioUrl = data.get("audioUrl")
    audioConfig = data.get("config")

    if not audioUrl:
        logging.info("no audioUrl")
    
    if not audioConfig:
        logging.info("no audio Config")

    if not audioUrl or not audioConfig:
        response = jsonify({"error": "no audioUrl or config"})
        response.status_code = 400
        return response

    logging.info("uri and config found")
    
    text = None
    try:
        logging.info("beginning audio processing")
        
        #logging.info(f"audio url: {audioUrl}")
        #logging.info(f"Length of audio_base64: {len(audioUrl)}")
        
        audio_bytes = base64.b64decode(audioUrl)
         
        logging.info("audio is inputted into the model")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
            logging.info("temp file made")
            tmp.write(audio_bytes)
            tmp.flush()
            tmp.seek(0)
            logging.info("audio written to temp file")
            text = speechToText(tmp.name)

        logging.info("model processing is completed")

        if text is None:
            response = jsonify({"error": "whisper speech translation failed"})
            response.status_code = 400
            return response
        
        logging.info(f"Model transcription complete: {text}")
        

    except Exception as e:
        logging.info("Error with speech detection")
        response = jsonify({"error": str(e)})
        response.status_code = 500
        return response
    
    
    logging.info("model chain is starting")
    try:
        logging.info(":)")
    except Exception as e:
        pass
        



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)