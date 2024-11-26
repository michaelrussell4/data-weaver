# pylint: disable=C0114, W0718

import os
import tomllib
import argparse
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    WikipediaLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    PyPDFLoader,
    CSVLoader,
    UnstructuredEPubLoader,
    UnstructuredMarkdownLoader,
)

# Ensure paths relative to this file's location.
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
config_path = os.path.join(parent_dir, "config.toml")
persist_directory = os.path.join(parent_dir, "chroma")
rag_docs_directory = os.path.join(parent_dir, "assets", "rag_docs")


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


def load_documents_from_directory(file_path: str) -> list:
    """Load the documents from the given local directory.

    Args:
        directory (str): Directory path.

    Returns:
        Documents: A list of documents loaded.
    """
    # Only process files
    ext = os.path.splitext(file_path)[-1].lower()

    # Use appropriate loader based on file extension
    loader = False
    match ext:
        case ".docx":
            loader = Docx2txtLoader(file_path)
        case ".xlsx":
            loader = UnstructuredExcelLoader(file_path)
        case ".pdf":
            loader = PyPDFLoader(file_path)
        case ".csv":
            loader = CSVLoader(file_path)
        case ".epub":
            loader = UnstructuredEPubLoader(file_path)
        case ".md":
            loader = UnstructuredMarkdownLoader(file_path)

    if not loader:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            loader = type(
                "loader",
                (object,),
                {
                    "load": lambda: [
                        Document(
                            page_content=content,
                            metadata={"source": file_path},
                        )
                    ]
                },
            )
        except Exception:
            if args.verbose:
                print(f"Skipping unsupported file: {file_path}")

    # Load the document and append it to the list
    docs = loader.load()

    return docs


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

    # Assuming load_documents_from_directory expects full file paths
    for file_name in os.listdir(rag_docs_directory):
        file_path = os.path.join(rag_docs_directory, file_name)
        if os.path.isfile(file_path):
            if args.verbose:
                print(f"Loading documents from {file_path}")
            docs.extend(load_documents_from_directory(file_path))

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
