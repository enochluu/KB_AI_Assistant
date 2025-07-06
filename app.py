import os
import re
import faiss
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer, CrossEncoder
from anthropic import Anthropic, APIConnectionError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize embedding and reranking models
model = SentenceTransformer('all-mpnet-base-v2')
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# --- Load documents from markdown files ---
def load_documents(folder_path="kb_articles"):
    documents = []
    filenames = []
    urls = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                lines = f.readlines()
                if not lines:
                    continue
                url = lines[0].strip()
                content = "".join(lines[1:]).strip()
                documents.append(content)
                filenames.append(filename)
                urls.append(url)

    return documents, filenames, urls

# --- Embed documents and build FAISS index ---
def create_faiss_index(documents):
    embeddings = model.encode(documents, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

@st.cache_data(show_spinner="🔍 Caching documents and index...")
def get_index_and_docs():
    docs, names, urls = load_documents()
    index = create_faiss_index(docs)
    return docs, names, urls, index

# --- Retrieve documents with FAISS + rerank with cross-encoder ---
def retrieve_documents(query, index, documents, filenames, urls, k=3, faiss_k=5):
    query_embedding = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_embedding, faiss_k)
    candidate_docs = [(filenames[idx], documents[idx], urls[idx]) for idx in I[0]]

    rerank_inputs = [(query, doc) for _, doc, _ in candidate_docs]
    scores = cross_encoder.predict(rerank_inputs)

    reranked = sorted(zip(candidate_docs, scores, D[0]), key=lambda x: x[1], reverse=True)
    top_k_docs = [(doc, rerank_score, faiss_score) for (doc, rerank_score, faiss_score) in reranked[:k]]

    return top_k_docs, None, None

# --- Generate answer from retrieved docs with source attribution ---
def generate_answer_claude(context_docs, query, api_key):
    if not context_docs:
        return "No relevant documents found to answer your question."

    summarized_docs = []
    for name, doc, url in context_docs:
        short_name = os.path.splitext(name)[0]
        summary = doc[:3000]
        summarized_docs.append((short_name, summary))

    context = "\n\n".join([f"{name}:\n{summary}" for name, summary in summarized_docs])

    system_prompt = (
        "You are a precise and obedient assistant. "
        "You must answer questions using only the provided documents. "
        "If relevant resolution steps are present in any document — even if brief or implicit — include them clearly in your answer. "
        "Do not provide general advice unless no document contains relevant information. "
    )

    prompt = f"""Human: You are a precise and obedient assistant. Based on the following summarized documents, answer the question below.

Documents:
{context}

Question: {query}

Assistant:"""

    client = Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            temperature=0.2,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        parts = [block.text for block in response.content if hasattr(block, 'text')]
        answer = "\n".join(parts) if parts else "Claude responded, but no text was returned."

        if "Sources:" not in answer:
            referenced = []
            for name, _, url in context_docs:
                short_name = os.path.splitext(name)[0]
                if short_name in answer:
                    referenced.append((short_name, url))

            if referenced:
                sources_md = "\n".join([f"- [{name}]({url})" for name, url in referenced])
                answer += f"\n\n📄 Sources:\n{sources_md}"

        return answer

    except APIConnectionError as e:
        st.error("⚠️ Claude API connection failed.")
        print("APIConnectionError:", e)
        return "Could not connect to Claude."
    except Exception as e:
        st.error("⚠️ Claude generation error.")
        print("Unexpected error:", e)
        st.text_area("Prompt Debug Info", prompt[:3000])
        return "An error occurred while generating the answer."

# --- Streamlit UI ---
st.title("🧠 AI-Powered KB Search with Claude 3.5, FAISS & Semantic RAG")
st.write("Ask natural language questions over your internal knowledge base. Backed by sentence-transformer embeddings, fast FAISS vector search, and Anthropic's Claude 3.5 for intelligent, document-grounded answers.")

api_key = ANTHROPIC_API_KEY
query = st.text_input("🔎 Ask a question:")

if query and api_key:
    with st.spinner("Running search..."):
        docs, names, urls, index = get_index_and_docs()

        if not docs:
            st.warning("No `.md` documents found in `kb_articles/`.")
        else:
            top_docs_with_scores, _, _ = retrieve_documents(query, index, docs, names, urls)
            top_docs = [doc for doc, _, _ in top_docs_with_scores]
            answer = generate_answer_claude(top_docs, query, api_key)

            st.subheader("💬 Answer:")
            st.write(answer)

            if top_docs_with_scores:
                st.subheader("📄 Top Matching Documents")
                for idx, ((name, doc, url), rerank_score, faiss_score) in enumerate(top_docs_with_scores):
                    short_name = os.path.splitext(name)[0]

                    # Vary excerpt length based on rank
                    excerpt_length = 800 if idx == 0 else 500 if idx == 1 else 400
                    excerpt = doc.strip()
                    if len(excerpt) > excerpt_length:
                        excerpt = excerpt[:excerpt_length].rstrip() + "..."

                    st.markdown(f"### {short_name} (Rank {idx + 1})")
                    st.markdown(f"[🔗 View Full Article]({url})")
                    st.write(f"**Rerank Score:** {rerank_score:.3f} | **FAISS Distance:** {faiss_score:.3f}")

                    with st.expander("Excerpt"):
                        st.markdown(excerpt, unsafe_allow_html=False)
            else:
                st.info("No documents matched your query.")
 