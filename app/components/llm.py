import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()


AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')
API_VERSION = os.environ.get('API_VERSION_LLM')

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    api_version=API_VERSION,
    temperature=0,
    streaming=True
)