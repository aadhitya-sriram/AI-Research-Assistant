import os
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from tools.pdf_ocr import run_ocr_on_file, needs_ocr

llm = Ollama(model="llama3.1:latest")
embeddings = OllamaEmbedding(model_name="tazarov/all-minilm-l6-v2-f32:latest")

def vectorize_pdf_data(pdf_path):
    pdf_name = pdf_path.split(".")[0].split("/")[-1]
    if pdf_name in os.listdir("data/vector_docs"):
        return f"Vectorized data for {pdf_path} already exists."
    else:
        reader = SimpleDirectoryReader(input_files=[pdf_path])
        documents = reader.load_data()

        if all(needs_ocr(doc.text) for doc in documents):
            documents = run_ocr_on_file(pdf_path)

        index = VectorStoreIndex.from_documents(documents, embed_model=embeddings)
        index.storage_context.persist(persist_dir=f"data/vector_docs/{pdf_name}")

def query_pdf_data(pdf_path, query):
    pdf_name = pdf_path.split(".")[0].split("/")[-1]
    if pdf_name in os.listdir("data/vector_docs"):
        storage_context = StorageContext.from_defaults(persist_dir=f"data/vector_docs/{pdf_name}")
        index = load_index_from_storage(storage_context, embed_model=embeddings)
        return index.as_query_engine(llm=llm).query(query) ####### ADD CONTEXT TO QUERY ENGINE
    else:
        return f"Vectorized data for {pdf_name} does not exists."

vectorize_pdf = FunctionTool.from_defaults(
    fn=vectorize_pdf_data,
    name="vectorize_pdf",
    description="Loads and processes PDF documents, extracts text, chunks content, and stores vector embeddings for efficient semantic retrieval."
)

query_pdf = FunctionTool.from_defaults(
    fn=query_pdf_data,
    name="query_pdf",
    description="Retrieves relevant information from previously vectorized PDF documents based on a natural language query using semantic search."
)


if __name__ == "__main__":
    pdf_path = "data/FLsample.pdf"
    query = "What is the main topic of the document?"
    vectorize_pdf_data(pdf_path)
    # result = query_pdf_data(pdf_path, query)
    # print(result)