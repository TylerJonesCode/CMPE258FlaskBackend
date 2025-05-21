from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import whisper

# Referenced this video in creating this section: https://www.youtube.com/watch?v=yF9kGESAi3M

GPT_model = ChatOpenAI(model="gpt-4o")
gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
speech_to_text_model = whisper.load_model("base")

def LLMRequestHandler(message):
    pass

def speechToText(file):
    return speech_to_text_model.transcribe(file)

def radioCommandTranslation(message):
    system_message = [
        SystemMessage(content="Instructions")
    ]

    response = GPT_model.invoke(system_message)
    return response.content

def flightManualAssistance(message):
    system_message = [
        SystemMessage(content="Instructions")
    ]

    response = GPT_model.invoke(system_message)
    return response.content
