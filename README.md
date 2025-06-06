# 🧠 AI Research Assistant

**A modular, extensible, and agent-powered personal research assistant built using the [LlamaIndex](https://github.com/jerryjliu/llama_index) ecosystem.**  
It runs locally on your Windows machine and leverages custom tools for PDF summarization, data analysis, translation, dictionary lookups, web search, and more.

---

## 📌 Features

- 🔍 **Semantic PDF Reader & Query Tool**  
  Load, vectorize, and semantically query scientific PDFs stored in your local system.

- 📊 **Tabular Data Analyzer**  
  Perform queries on CSV, Excel, Parquet, SQLite, and JSON files using natural language.

- 📝 **Note Taker**  
  Automatically saves notes with time-stamped, structured filenames.

- 🌐 **Web Search**  
  Uses DuckDuckGo (via `ddgs`) for simple and quick online lookups.

- 🌍 **Language Translator**  
  Translate text into any language using Google Translate.

- 📚 **Dictionary Tool**  
  Fetch detailed word definitions and examples via an open dictionary API.

- 📑 **PDF Summarizer**  
  Generate structured summaries of large documents using custom summarization prompts.

---

## 🏗️ Directory Structure

```
aadhitya-sriram-ai-research-assistant/
├── main.py                  # Entry point: starts ReActAgent loop
├── prompts.py              # Agent instructions and summarization prompt
├── requirements.txt        # Project dependencies
├── test.py                 # Script to test summarization independently
└── tools/
    ├── bibliography.py     # Placeholder (future)
    ├── dictionary.py       # Fetches word meanings via API
    ├── file_searcher.py    # Locates files in the data/ folder
    ├── note_taker.py       # Saves text notes to notes/ folder
    ├── pandas_analyzer.py  # Queries tabular data using LLM and pandas
    ├── pdf_ocr.py          # OCR for image-based PDFs
    ├── pdf_reader.py       # Vectorizes and queries PDFs
    ├── summarizer.py       # Structured summarization of PDF content
    ├── translator.py       # Async translation using Google Translate
    ├── visualizer.py       # Placeholder (future)
    └── web_search.py       # Performs DuckDuckGo-based web search
```

---

## ⚙️ Installation

> This project is designed for **Python 3.10+**.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/aadhitya-sriram-ai-research-assistant.git
cd aadhitya-sriram-ai-research-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the root directory for keys and config (optional).

```env
# Example: If using GROQ or other APIs
API_KEY=your_key_here
```

---

## 🚀 Usage

### Run the Assistant

```bash
python main.py
```

You'll be prompted to enter natural language queries.  
The agent selects the appropriate tool and responds accordingly.

---

## 🧠 Agent Design

- **Framework**: [LlamaIndex ReActAgent](https://docs.llamaindex.ai/en/stable/)
- **LLM**: [Ollama](https://ollama.com) with `llama3.1:latest` (can be replaced with Groq)
- **Tools**:
  - `note_saver`: Save notes
  - `data_analysis`: Query structured tabular files
  - `dictionary_tool`: Fetch dictionary definitions
  - `translate_text`: Translate text asynchronously
  - `web_search`: Search the web
  - `vectorize_pdf` / `query_pdf`: Index and query PDF documents
  - `summarize_pdf`: Produce structured summaries (direct response)

---

## 📁 Data Organization

- PDF files and structured data go into the `data/` folder.
- Vectorized documents are stored in `data/vector_docs/`.
- Notes are saved in the `notes/` directory organized by year/month.

---

## 🔧 Future Enhancements

- Add bibliography parsing and citation manager
- Build a UI with Streamlit or Gradio
- Enable visual chart generation in `visualizer.py`
- OCR fallback for scanned PDFs is partially implemented
- Live documentation at `/docs`

---

## 📜 License

MIT License © 2025 Aadhitya Sriram

---

## 🙌 Acknowledgements

- [LlamaIndex](https://github.com/jerryjliu/llama_index)
- [Ollama](https://ollama.com)
- [Google Translate](https://pypi.org/project/googletrans/)
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)
