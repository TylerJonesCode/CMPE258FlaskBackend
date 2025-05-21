from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
import openai

# Referenced this video in creating this section: https://www.youtube.com/watch?v=yF9kGESAi3M

# GPT_model = ChatOpenAI(model="gpt-4o")
# gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# model = gemini_model

# classifier_prompt_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", """You are an assistant that will classify the types of prompts by pilots that are sent to you. 
#                         """),
#         ("human", {"""You must assign the following prompt exactly one number from 0-2. 
#                       Assign a 1 if the request is for radio command translation.
#                       Assign a 2 if the request is for flight manual assistance.
#                       Assign a 0 if the request is for anything else: 
#                       {prompt}"""})
        
#     ]
# )


# radio_command_translation_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are an assistant that will decode the radio command sent by the user and explain in detail what it means."),
#         ("human", "{prompt}")
#     ]
# )


# radio_command_translation_better = RunnableLambda(

# )

# flight_manual_assistance_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are an assistant that will assist pilots with their questions related to flight manuals. Answer their questions in detail."),
#         ("human", "{prompt}")
#     ]
# )

# general_assistance_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are an assistant that will classify the types of prompts by pilots that are sent to you."),
#         ("human", "{prompt}")
#     ]
# )

# task_branches = RunnableBranch(
#     (
#         lambda x: "1" in x,
#         radio_command_translation_template | model | StrOutputParser
#     ),
#     (
#         lambda x: "2" in x,
#         flight_manual_assistance_template | model | StrOutputParser
#     ),
#     general_assistance_template | model | StrOutputParser
# )

# classifier_chain = classifier_prompt_template | model | StrOutputParser

# request_chain = classifier_chain | task_branches

def LLMRequestHandler(prompt):
    #response = request_chain.invoke({"prompt": prompt})
    pass
def speechToText(file):
    text = openai.Audio.transcribe(
                model="whisper-1",
                file=file
            )
    return text

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
