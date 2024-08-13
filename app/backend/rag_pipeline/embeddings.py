import os
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


AZURE_OPENAI_API_KEY_EMBEDDINGS = os.environ.get('AZURE_OPENAI_API_KEY_EMBEDDINGS')
AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDINGS = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDINGS')
AZURE_ENDPOINT_EMBEDDINGS = os.environ.get('AZURE_ENDPOINT_EMBEDDINGS')
API_VERSION_EMBEDDINGS = os.environ.get('API_VERSION_EMBEDDINGS')

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=AZURE_ENDPOINT_EMBEDDINGS,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDINGS,
    api_key=AZURE_OPENAI_API_KEY_EMBEDDINGS,
    api_version=API_VERSION_EMBEDDINGS
)