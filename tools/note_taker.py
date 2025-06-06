import os
from datetime import datetime
from llama_index.core.tools import FunctionTool

def save_note(note_text):
    """
    Saves a note into a date-based directory structure.
    
    Parameters:
        note_text (str): The content of the note.
        base_dir (str): The root folder where notes are stored.
        fmt (str): File format - 'md' for Markdown, 'txt' for plain text.
    
    Output:
        File path of saved note.
    """

    base_dir = "./notes"

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    year = now.strftime("%Y")
    month = now.strftime("%m-%B")

    directory = os.path.join(base_dir, year, month)
    os.makedirs(directory, exist_ok=True)

    filename = f"{date_str}.txt"
    file_path = os.path.join(directory, filename)

    with open(file_path, "a", encoding="utf-8") as f:
        f.writelines([note_text.strip() + "\n"])

    print(f"Note saved to {file_path}")

note_tool = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="this tool can save a text based note to a file for the user",
)