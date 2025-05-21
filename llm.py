from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableBranch, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
import openai
import logging

# Referenced this video in creating this section: https://www.youtube.com/watch?v=yF9kGESAi3M

# GPT_model = ChatOpenAI(model="gpt-4o")
# gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# model = gemini_model

classifier_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """You are an assistant that will classify the types of prompts by pilots that are sent to you. 
                        """),
        ("human", """You must assign the following prompt exactly one number from 0-2. 
                      Assign a 1 if the request is for radio command translation.
                      Assign a 2 if the request is for flight manual assistance.
                      Assign a 0 if the request is for anything else: 
                      {prompt}""")
        
    ]
)


radio_command_translation_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant that will decode the radio command sent by the user and explain in detail what it means."),
        ("human", "{prompt}")
    ]
)

#
#radio_command_translation_better = RunnableLambda(
#
#)

flight_manual_assistance_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant that will assist pilots with their questions related to flight manuals. Answer their questions in detail."),
        ("human", "{prompt}")
    ]
)

general_assistance_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant that will answer the types of prompts by pilots that are sent to you."),
        ("human", "{prompt}")
    ]
)

model = None
def get_model():
    global model
    if model is None:
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    return model

chain = None
def get_chain():
    global chain
    if chain is None:
        curr_model = get_model()
        classification = RunnableLambda(lambda prompt: {
            "prompt": prompt,
            "classification": (prompt | classifier_prompt_template | curr_model | StrOutputParser()).invoke(prompt)
        })
        task_branches = RunnableBranch(
            (
                lambda x: "1" in x["classification"],
                RunnableLambda(lambda x: (radio_command_translation_template | curr_model | StrOutputParser()).invoke(x["prompt"]) )
            ),
            (
                lambda x: "2" in x["classification"],
                RunnableLambda(lambda x: (flight_manual_assistance_template | curr_model | StrOutputParser()).invoke(x["prompt"]))
            ),
            RunnableLambda(lambda x: (general_assistance_template | curr_model | StrOutputParser()).invoke(x["prompt"]))
        )


        chain = classification | task_branches

    return chain

def LLMRequestHandler(prompt):
    logging.info(f"Request handling started. Prompt: {prompt}")
    llm_chain = get_chain()
    response = llm_chain.invoke({"prompt": prompt})
    logging.info(f"Request handled. Result: {response}")
    return response
def speechToText(file):
    logging.info("API request is being sent")
    try:
        text = None
        client = openai.OpenAI()
        with open(file, "rb") as audio_file:
            text = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        logging.info("API result was received")
        return text.text
    except Exception as e:
        logging.info(e)
        return ""
    
    

def radioCommandTranslation(message):
    system_message = [
        SystemMessage(content="Instructions")
    ]

    response = model.invoke(system_message)
    return response.content

def flightManualAssistance(message):
    system_message = [
        SystemMessage(content="Instructions")
    ]

    response = model.invoke(system_message)
    return response.content

def LLMTesting(message):
    model = get_model()
    response = model.invoke(message)

    model = ChatOpenAI(model="gpt-4o")
    response = model.invoke(message)
