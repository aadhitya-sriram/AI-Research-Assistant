import os
from llama_index.core.tools import FunctionTool

def find_file(filename: str) -> str:
    """
    Walk `directory` (and subfolders) looking for `filename`.
    Returns the full path if found, or raises FileNotFoundError.
    """
    directory = "data"
    for root, _, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    raise FileNotFoundError(f"{filename} not found in {directory!r}")

find_file_tool = FunctionTool.from_defaults(
    fn=find_file,
    name="find_file",
    description="Given a filename, returns the full path to that file on disk."
)