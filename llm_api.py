"""
This module provides a Flask API endpoint for querying a Retrieval Augmented Generation (RAG) 
system powered by Ollama and Chroma.

### Example:

```python
import requests

api_url = "http://127.0.0.1:5000/query"  # Replace with your Flask app URL
input_value = 'hey tell me a very short story about a rabbit and a snake'
response = requests.post(api_url, json={"input": input_value})
response.raise_for_status()  # Raise an error for HTTP issues
data = response.json()
data_out = data.get('response', 'No response received')
```
"""

# pylint: disable=W0718

import tomllib
from flask import Flask, request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Load config
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# Get vectorstore
embedding_model_id = config["utils"]["chroma"]["embedding_model_id"]
collection_name = config["utils"]["chroma"]["collection_name"]
embedding_model = OllamaEmbeddings(model=embedding_model_id)
vectorstore = Chroma(
    collection_name=collection_name,
    embedding_function=embedding_model,
    persist_directory="chroma",
)
retriever = vectorstore.as_retriever()

# Build LLM and RAG chain
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", config["llm"]["system_prompt"]),
        ("human", "{input}"),
    ]
)
llm = ChatOllama(model=config["llm"]["model_id"], **config["llm"]["chat_kwargs"])
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

app = Flask(__name__)


def format_result(result):
    """Format the result appropriately for jsonify."""
    context_metadata = [doc.metadata for doc in result.get("context", [])]
    return {
        "input": result.get("input"),
        "context": context_metadata,
        "answer": result.get("answer"),
    }


@app.route("/query", methods=["POST"])
def query():
    """Endpoint for querying the LLM."""
    data = request.json
    input_text = data.get("input")
    if not input_text:
        return jsonify({"error": "Missing 'input' in request"}), 400

    # Run the chain
    try:
        result = rag_chain.invoke({"input": input_text})
        formatted_result = format_result(result)
        return jsonify({"response": formatted_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host=config["llm"]["host"], port=config["llm"]["port"])
