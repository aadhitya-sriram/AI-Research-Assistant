import sys
import requests
from llama_index.core.tools import FunctionTool

def get_definitions(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    try:
        data = response.json()
    except ValueError:
        return "Error: Invalid JSON response."

    if isinstance(data, dict) and data.get("title") == "No Definitions Found":
        return f"\nNo definitions found for '{word}'."

    def_string = f"Definitions for: {data[0]['word']}\n"

    for meaning in data[0].get("meanings", []):
        part_of_speech = meaning.get("partOfSpeech", "unknown")
        def_string += f"\n{part_of_speech.title()}\n"

        for i, definition in enumerate(meaning.get("definitions", []), 1):
            def_string += f" {i}. {definition['definition']}\n"
            if "example" in definition:
                def_string += f"    Example: {definition['example']}"

    return {"Meaning": def_string.strip()}

dictionary_tool = FunctionTool.from_defaults(
    fn=get_definitions,
    name="dictionary_tool",
    description="Get dictionary definitions for a word as a JSON."
)