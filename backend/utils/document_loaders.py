import os
import hashlib
from typing import List, Dict, Optional, Tuple

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Embeddings via local Ollama
import ollama

# Pinecone client
try:
    # Prefer modern pinecone package if available
    from pinecone import Pinecone
    _PINECONE_V3 = True
except Exception:
    # Fallback to older client
    from pinecone import Index, PineconeException, init as pinecone_init
    _PINECONE_V3 = False


def load_document_loader(file_path: str):
    """Return an appropriate LangChain loader for the given file path."""
    if file_path.endswith('.pdf'):
        return PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        return Docx2txtLoader(file_path)
    elif file_path.endswith('.txt'):
        return TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file_path}")


def load_and_split(file_path: str,
                   chunk_size: int = 800,
                   chunk_overlap: int = 120) -> List[Document]:
    """
    Load a document from disk and split into smaller chunks.
    Returns a list of LangChain Document objects.
    """
    loader = load_document_loader(file_path)
    raw_docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(raw_docs)

    # Attach simple source metadata if missing
    for idx, doc in enumerate(documents):
        doc.metadata = doc.metadata or {}
        doc.metadata.setdefault("source", os.path.basename(file_path))
        doc.metadata.setdefault("chunk", idx)

    return documents


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def embed_texts_ollama(texts: List[str], model: str = "mxbai-embed-large") -> List[List[float]]:
    """
    Generate embeddings for a list of texts using a local Ollama model.
    Requires the Ollama daemon to be running and the model pulled.
    """
    embeddings: List[List[float]] = []
    for text in texts:
        response = ollama.embeddings(model=model, prompt=text)
        embeddings.append(response["embedding"])  # type: ignore[index]
    return embeddings


def _get_pinecone_index(index_name: Optional[str] = None):
    """Initialize and return a Pinecone index handle."""
    api_key = os.environ.get("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY is not set in environment")

    resolved_index = index_name or os.environ.get("PINECONE_INDEX_NAME")
    if not resolved_index:
        raise RuntimeError("PINECONE_INDEX_NAME not provided and not set in environment")

    if _PINECONE_V3:
        pc = Pinecone(api_key=api_key)
        return pc.Index(resolved_index)
    else:
        # Older client path (kept for compatibility)
        pinecone_env = os.environ.get("PINECONE_ENVIRONMENT")
        if not pinecone_env:
            raise RuntimeError("PINECONE_ENVIRONMENT must be set for legacy pinecone client")
        pinecone_init(api_key=api_key, environment=pinecone_env)
        return Index(resolved_index)


def upsert_documents_to_pinecone(documents: List[Document],
                                 index_name: Optional[str] = None,
                                 namespace: Optional[str] = None,
                                 model: str = "mxbai-embed-large") -> Tuple[int, str]:
    """
    Create embeddings for provided Documents and upsert into Pinecone.
    - Each vector id is derived from a stable hash of the content.
    - Metadata includes `source` and `chunk` by default.

    Returns (num_vectors_upserted, index_name_used)
    """
    if not documents:
        return 0, (index_name or os.environ.get("PINECONE_INDEX_NAME") or "")

    texts = [d.page_content for d in documents]
    vectors = embed_texts_ollama(texts, model=model)

    index = _get_pinecone_index(index_name)

    items = []
    for doc, vector in zip(documents, vectors):
        vector_id = _hash_text(doc.page_content)
        metadata: Dict = {**(doc.metadata or {})}
        metadata.setdefault("source", metadata.get("source", "unknown"))
        metadata.setdefault("chunk", metadata.get("chunk", 0))
        items.append({
            "id": vector_id,
            "values": vector,
            "metadata": metadata
        })

    # Upsert depending on client flavor
    if _PINECONE_V3:
        index.upsert(vectors=items, namespace=namespace)
    else:
        index.upsert(vectors=items, namespace=namespace)  # same signature in older client

    return len(items), getattr(index, "_name", os.environ.get("PINECONE_INDEX_NAME") or "")


def process_and_index(file_path: str,
                      index_name: Optional[str] = None,
                      namespace: Optional[str] = None,
                      chunk_size: int = 800,
                      chunk_overlap: int = 120,
                      model: str = "mxbai-embed-large") -> Tuple[int, str]:
    """
    High-level helper that:
    1) Loads and splits a document
    2) Generates embeddings with Ollama mxbai-embed-large
    3) Upserts vectors into Pinecone
    Returns (num_vectors_upserted, index_name_used)
    """
    docs = load_and_split(file_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return upsert_documents_to_pinecone(docs, index_name=index_name, namespace=namespace, model=model)
