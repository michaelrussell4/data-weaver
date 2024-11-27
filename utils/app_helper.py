"""Helper functions and variables for the Dash app."""

import os
from urllib.parse import urlparse
import tomllib
from itertools import cycle
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import pandas as pd

# Load config
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

COLOR_PALETTE = cycle(
    [
        "bg-blue-400",  # Blue
        "bg-purple-400",  # Purple
        "bg-green-400",  # Green
        "bg-teal-400",  # Teal
        "bg-indigo-400",  # Indigo
    ]
)

# Get vectorstore
embedding_model_id = config["utils"]["chroma"]["embedding_model_id"]
collection_name = config["utils"]["chroma"]["collection_name"]
embedding_model = OllamaEmbeddings(model=embedding_model_id)
vectorstore = Chroma(
    collection_name=collection_name,
    embedding_function=embedding_model,
    persist_directory="chroma",
)


def is_url(input_string: str) -> bool:
    """
    Determines if the input string is a file path or a URL.

    Args:
        input_string (str): The string to evaluate.

    Returns:
        str: "file_path" if the input is a file path,
             "url" if the input is a URL,
             "unknown" if it doesn't match either.
    """
    # Check for URL using urlparse
    parsed = urlparse(input_string)
    if parsed.scheme in ["http", "https", "ftp"] and parsed.netloc:
        return True

    return False


def get_file_extension(file_path: str, default_ext: str = "unknown") -> str:
    """
    Returns the file extension from a file path without the dot.
    If no extension is found, returns 'unknown'.

    Args:
        file_path (str): The file path string.

    Returns:
        str: The file extension (e.g., 'docx'), or 'unknown' if none is found.
    """
    _, ext = os.path.splitext(file_path)
    return ext[1:] if ext else default_ext


def get_source_type(source: str) -> str:
    if is_url(source):
        return "url"
    else:
        return get_file_extension(source)


chroma_df = pd.DataFrame(
    [v["source"] for v in vectorstore.get()["metadatas"]], columns=["source"]
)
chroma_df["ext"] = chroma_df.source.apply(get_source_type)
