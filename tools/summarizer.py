import os
import httpx
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from prompts import summary_prompt
from tools.pdf_reader import vectorize_pdf
from llama_index.core import PromptTemplate
from ollama import chat, ChatResponse

# llm = Ollama(model="llama3.1:latest", timeout=120)
embeddings = OllamaEmbedding(model_name="tazarov/all-minilm-l6-v2-f32:latest")

def get_pdf_content(pdf_path: str) -> str:
    """
    Retrieve and concatenate content from a vectorized PDF document.
    """
    pdf_name = pdf_path.split(".")[0].split("/")[-1]
    
    if pdf_name not in os.listdir("data/vector_docs"):
        vectorize_pdf(pdf_path)
    
    storage_context = StorageContext.from_defaults(persist_dir=f"data/vector_docs/{pdf_name}")
    index = load_index_from_storage(storage_context, embed_model=embeddings)
    
    all_docs = index.docstore.docs.values()
    
    content = []
    for doc in sorted(all_docs, key=lambda x: int(x.metadata.get('page', 0))):
        page_num = doc.metadata.get('page_label', 'Unknown')
        content.append(f"Page {page_num}:\n{doc.text}\n")
    
    return content
    
def get_pdf_text(pdf_path: str) -> str:
    """
    Retrieve and concatenate text content from a vectorized PDF document.
    """
    content = get_pdf_content(pdf_path)
    return "\n".join(content)

def summarize_pdf_content(pdf_path):
    content = get_pdf_content(pdf_path)
    text = "\n".join(content)
    summary = summary_prompt.format(pdf_text=text)

    
    response: ChatResponse = chat(model='llama3.1:latest', messages=[{'role': 'user','content': summary}])
    return {"summary" : response['message']['content']}

    # max_retries = 3
    # for attempt in range(max_retries):
    #     try:
    #         response = llm.complete(summary)
    #         return response
    #     except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
    #         if attempt == max_retries - 1:
    #             raise
    #         continue

get_pdf_content_tool = FunctionTool.from_defaults(
    fn=get_pdf_text,
    name="get_pdf_text",
    description="Retrieves the full content from a PDF document organized by page numbers. Automatically vectorizes the PDF if not already processed."
)

summary_tool = FunctionTool.from_defaults(
    fn=summarize_pdf_content,
    name="summarize_pdf",
    description="Generates a structured summary of a PDF document including title, overview, and key points which is to be given to the user directly.",
    return_direct=True
)

# Stream the Response



# if __name__ == "__main__":
#     pdf_path = "data/cnsppt.pdf"
#     result = summarize_pdf_content(pdf_path)
#     print(result)