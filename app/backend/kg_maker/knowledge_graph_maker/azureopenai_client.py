from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from knowledge_graph_maker.types import LLMClient
from dotenv import dotenv_values

config = dotenv_values(".env")

class AzureOpenAIClient(LLMClient):
    
    def __init__(
        self, temperature=0
    ):
        self._temperature = temperature
        self.client = AzureChatOpenAI(
            azure_endpoint=config['AZURE_ENDPOINT'],
            api_key=config['AZURE_OPENAI_API_KEY'],
            azure_deployment=config['AZURE_OPENAI_DEPLOYMENT_NAME'],
            api_version=config['API_VERSION_LLM'],
            temperature=self._temperature,
            streaming=True
        )
        self.prompt = PromptTemplate(
            input_variables=['system_message', 'user_message'],
            template= "System message: {system_message}, User message: {user_message}"
        )

    def generate(self, user_message: str, system_message: str) -> str:
        prompt_formatted_str = self.prompt.format(system_message=system_message, user_message=user_message)
        return self.client.invoke(prompt_formatted_str).content