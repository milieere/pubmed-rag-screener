### Welcome to the PoC scientific ChatBot repo!

- This project features a scientific chatbot built with Streamlit, Langchain, and ChatGPT.
- To run this project as it is, you will need access to AzureOpenAI ChatGPT model and ADA embeddings model.
- Alternatively, you can switch the LLM to any other LLM model available via langchain interfaces (i.e. ChatGPT and embedding models available via OpenAI directly).
- To plug in your own LLM and embeddings, please modify the following files:
    - /app/components/llm.py to edit LLM
    - /backend/rag_pipeline/embeddings.py

#### Environment variables
- Handle your environment variables (API keys and credentials) in a .env file and use python-dotenv to retrieve them. Example .env file (with AzureOpenAI variables) can look like this:

```
AZURE_OPENAI_API_KEY=<llm-api-key>
AZURE_OPENAI_DEPLOYMENT_NAME=<llm-deployment-name>
AZURE_ENDPOINT=<llm-api-endpoint>
API_VERSION=<llm-api-version>

AZURE_OPENAI_API_KEY_EMBEDDINGS=<embeddings-api-key>
AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDINGS=<embeddings-deployment-name>
AZURE_ENDPOINT_EMBEDDINGS=<embeddings-endpoint>
API_VERSION_EMBEDDINGS=<embeddings-api-version>
```

#### Environment installation

In the project root directory, create virtual environment using venv, and install dependencies from environment/requirements.txt file:

```
python -m venv venv
source venv/bin/activate
pip install -r environment/requirements.txt
```

#### Run application

- Navigate to the app submodule of the repo `cd app`
- Run the streamlit application `streamlit run app.py`
- Navigate in your browser to `http://localhost:8501`
- Have fun!
