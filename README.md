# AI-Powered Knowledge Base Search

This project provides a Streamlit web app that enables natural language question answering over your internal knowledge base.

It uses:
- **Sentence-Transformers** to embed markdown documents
- **FAISS** for fast vector similarity search
- **Anthropic Claude 3.5** for generating intelligent, document-grounded answers with source attribution
- **Streamlit** for a simple and interactive UI

---

## Features

- Load `.md` files from the `kb_articles` folder, extracting URLs and content
- Create and cache embeddings for efficient semantic search
- Retrieve top relevant documents via FAISS + cross-encoder reranking
- Generate precise answers from retrieved documents using Claude 3.5 API
- Display answers along with top matching documents and excerpts

---

## How to use

1. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    # Windows (Git Bash or PowerShell)
    source venv/Scripts/activate
    # macOS/Linux
    source venv/bin/activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set your Claude API key in a `.env` file at the root:

    ```
    ANTHROPIC_API_KEY=your_api_key_here
    ```

4. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

5. Ask questions in the app UI and get answers based on your knowledge base.

---

## Notes

- Place your markdown knowledge base files in the `kb_articles` folder.
- The first line of each `.md` file should be the URL of the document.
- Excerpts and source links are shown with the answers for transparency.

---

## License

[Add your license here]

