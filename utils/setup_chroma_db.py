# pylint: disable C0114

import os
import tomllib
import argparse
from langchain_chroma import Chroma
from langchain_community.document_loaders import WikipediaLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Ensure paths relative to this file's location.
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
config_path = os.path.join(parent_dir, "config.toml")
persist_directory = os.path.join(parent_dir, "chroma")

# Load config.
with open(config_path, "rb") as f:
    config = tomllib.load(f)
embedding_model_id = config["utils"]["chroma"]["embedding_model_id"]
config_wiki = config["utils"]["chroma"]["wikipedia"]

# Set up argument parser for verbose mode
parser = argparse.ArgumentParser(
    description="Load/refresh Chroma DB with Wikipedia articles."
)
parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose output for debugging"
)
args = parser.parse_args()


def main():
    """Load/refresh the chroma db locally based on articles from config and document search path."""
    if args.verbose:
        print("Verbose mode enabled.")
        print(f"Loading configuration from {config_path}")

    docs = []
    if args.verbose:
        print("Starting Wikipedia article loading...")

    for query in config_wiki["queries"]:
        if args.verbose:
            print(f"Loading documents for query: {query}")
        docs.extend(
            WikipediaLoader(
                query=query, load_max_docs=config_wiki["load_max_docs"]
            ).load()
        )

    if args.verbose:
        print(f"Total documents loaded: {len(docs)}")
        print("Splitting documents into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config_wiki["chunk_size"], chunk_overlap=config_wiki["chunk_overlap"]
    )
    splits = text_splitter.split_documents(docs)

    if args.verbose:
        print(f"Total document chunks created: {len(splits)}")
        print(f"Embedding model: {embedding_model_id}")

    embedding = OllamaEmbeddings(model=embedding_model_id)
    vectorstore = Chroma(
        embedding_function=embedding, persist_directory=persist_directory
    )

    if args.verbose:
        print(f"Persisting documents to Chroma DB in {persist_directory}...")

    vectorstore.add_documents(splits)

    if args.verbose:
        print("Chroma DB updated successfully.")


if __name__ == "__main__":
    main()
