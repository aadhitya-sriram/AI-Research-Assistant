import os
from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.llms.groq import Groq
from tools.pandas_analyzer import tabular_tool
from tools.file_searcher import find_file_tool
from tools.note_taker import note_tool
from tools.dictionary import dictionary_tool
from tools.translator import translate_tool
from tools.web_search import web_tool
from tools.pdf_reader import vectorize_pdf, query_pdf
from tools.summarizer import summary_tool, get_pdf_content_tool
from prompts import agent_context

load_dotenv()
os.makedirs("data/", exist_ok=True)
os.makedirs("data/vector_docs", exist_ok=True)
os.makedirs("notes/", exist_ok=True)

tools = [
    note_tool,
    find_file_tool,
    tabular_tool,
    dictionary_tool,
    translate_tool,
    web_tool,
    vectorize_pdf, 
    query_pdf, 
    summary_tool, 
    get_pdf_content_tool
]

llm = Ollama(model="llama3.1:latest")
# llm = Groq(model="llama-3.1-8b-instant")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, system_prompt=agent_context, timeout=120)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    try:
        answer = agent.query(prompt)
        print(answer)
    except ValueError as e:
        if "max iterations" in str(e):
            print("⚠️ Agent didn't converge—try increasing max_iterations or refining your prompt.")
            answer = None