import pandas as pd
import sqlite3
import json
import os
from prompts import pandas_instr_prompt, pandas_prompt
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import ToolMetadata
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.llms.groq import Groq
from dotenv import load_dotenv

load_dotenv()
llm = Ollama(model="llama3.1:latest")
# llm = Groq(model="llama-3.1-8b-instant")

def analyze_tabular(file_path: str, query: str):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
    elif ext == ".json":
        df = pd.read_json(file_path)
    elif ext == ".parquet":
        df = pd.read_parquet(file_path)
    elif ext == ".db":  # or .sqlite
        conn = sqlite3.connect(file_path)
        table_name = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn).iloc[0, 0]
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    query_engine = PandasQueryEngine(df=df, llm=llm, verbose=True, instruction_str=pandas_instr_prompt)
    query_engine.update_prompts({"pandas_prompt": pandas_prompt})
    
    response = query_engine.query(query)
    return str(response)

tabular_tool = FunctionTool.from_defaults(
    fn=analyze_tabular,
    name="data_analysis",
    description="Analyse a CSV/Excel/JSON/Parquet/SQLite file and ask any question about its data."
)


# def build_tabular_tool(file_path: str, tool_name: str, description: str) -> QueryEngineTool:
#     query_engine = load_tabular_file(file_path)
#     return QueryEngineTool(
#         query_engine=query_engine,
#         metadata=ToolMetadata(
#             name=tool_name,
#             description=description,
#         )
#     )