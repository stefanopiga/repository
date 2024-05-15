"""configurazione modello linguistico"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

# Istanze LLM
llm_gpt4 = ChatOpenAI(model="gpt-4")
llm_gpt3_5 = ChatOpenAI(model="gpt-3.5-turbo")
