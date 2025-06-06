import asyncio
from googletrans import Translator
from llama_index.core.tools import FunctionTool

async def translate_text(text, target_language='en'):
    async with Translator() as translator:
        result = await translator.translate(text, dest=target_language)
        return result.text

translate_tool = FunctionTool.from_defaults(
    async_fn=translate_text,
    name="translate_text",
    description="Translates given text to a specified target language."
)

# print(asyncio.run(translate_text('Hola, ¿cómo estás?', target_language='en')))