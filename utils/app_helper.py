"""Helper functions and variables for the Dash app."""

import os
import requests
from urllib.parse import urlparse
import tomllib
from itertools import cycle
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import pandas as pd
from dash import html
from dash_iconify import DashIconify
import dash_mantine_components as dmc

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
EXT_COLOR_MAP = {}


def chat_ai(input_text):
    api_url = "http://127.0.0.1:5000/query"  # Replace with your Flask app URL
    response = requests.post(api_url, json={"input": input_text})
    response.raise_for_status()  # Raise an error for HTTP issues
    data = response.json()
    data_out = data.get("response", "No response received")
    return data_out["answer"]


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


def get_file_icon(file_name):
    # Map file extensions or URLs to appropriate icons
    extension_icons = {
        ".docx": "mdi:file-word-outline",
        ".xlsx": "mdi:file-excel-outline",
        ".pdf": "mdi:file-pdf-outline",
        ".csv": "mdi:file-delimited-outline",
        ".txt": "mdi:file-document-outline",
        ".md": "mdi:language-markdown",
        ".epub": "mdi:file-book-outline",
    }
    if file_name.startswith("http"):  # Handle URLs
        return "mdi:web"
    ext = os.path.splitext(file_name)[-1].lower()
    return extension_icons.get(
        ext, "mdi:file-outline"
    )  # Default icon for unknown types


def make_file_display(file_path):
    # Check if the path is a URL
    file_is_url = file_path.startswith("http")

    # Extract the file name (include extension if it's a file)
    if file_is_url:
        file_name = file_path.split("/")[-1]
    else:
        file_name = os.path.basename(file_path)

    # Truncate file name for aesthetic purposes
    display_name = file_name if len(file_name) <= 20 else file_name[:12] + "..."

    return html.A(
        href=file_path,
        target="_blank",
        title=file_name,  # Set the full file name or URL as the tooltip
        className=(
            "flex flex-col justify-center items-center text-center p-1 pt-2 border "
            "rounded-lg shadow-sm hover:shadow-lg h-24 bg-gray-100 gap-2"
        ),
        children=[
            DashIconify(
                icon=get_file_icon(file_path), width=30, className="text-indigo-900"
            ),
            html.Div(display_name, className="text-sm"),
        ],
    )


def create_message(message, icon, icon_right=False):
    icon_comp = DashIconify(
        icon=icon,
        width=30,
        className=f"text-indigo-500 text-3xl z-20 m{"l" if icon_right else "r"}-2 bg-white",
    )
    msg_comp = html.Div(
        message,
        className=f"bg-{"blue" if icon_right else "gray"}-100 shadow-sm rounded-xl p-4 text-gray-500 z-10",
        style={
            "white-space": "pre-wrap",  # Only break on newlines unless forced
            "word-wrap": "break-word",  # Break words if constrained
            "width": "fit-content",  # Adjust width to fit content
            "max-width": "66.6666%",  # Max width is 2/3 of the parent
        },
    )
    children = [icon_comp, msg_comp]
    if icon_right:
        children = children[::-1]
    return html.Div(
        className=f"mt-6 flex justify-{"end" if icon_right else "start"}",
        children=children,
    )


def create_weaver_message(message):
    return create_message(message, "mdi:robot-outline")


def create_user_message(message):
    return create_message(message, "mdi:account", True)


def make_ext_button(ext):
    """
    Creates a button for a file extension with a unique color.

    Args:
        ext (str): The file extension.

    Returns:
        dmc.Button: A styled button with a unique color for the extension.
    """
    # Assign a color to the extension if not already assigned
    if ext not in EXT_COLOR_MAP:
        EXT_COLOR_MAP[ext] = next(COLOR_PALETTE)

    # Create the button with the assigned color
    return dmc.Button(
        ext,
        id={"type": "ext-button", "index": ext},
        radius="xl",
        className=f"text-center text-white {EXT_COLOR_MAP[ext]}",
    )


def make_df_from_vectorstore(search: str = None):
    if search:
        sources = [
            doc.metadata["source"] for doc in vectorstore.similarity_search(search)
        ]
    else:
        sources = [v["source"] for v in vectorstore.get()["metadatas"]]
    _chroma_df = pd.DataFrame(sources, columns=["source"])
    _chroma_df["ext"] = _chroma_df.source.apply(get_source_type)

    return _chroma_df


chroma_df = make_df_from_vectorstore()
