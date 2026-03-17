import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

def get_vectorstore(persist_directory: str = "./chroma_db"):
    # Using open-source free local embeddings 
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma(embedding_function=embeddings, persist_directory=persist_directory)

def ingest_papers(paper_paths: list[str], persist_directory: str = "./chroma_db"):
    vectorstore = get_vectorstore(persist_directory)
    # RecursiveCharacterTextSplitter per given configuration
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    for path in paper_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            chunks = splitter.create_documents([content], metadatas=[{"source": path}])
            vectorstore.add_documents(chunks)
            print(f"Ingested {path}")
        else:
            print(f"File not found: {path}")

def retrieve_context(query: str, k: int = 5, persist_directory: str = "./chroma_db") -> str:
    vectorstore = get_vectorstore(persist_directory)
    # Setup similarity search to extract relevant snippets
    docs = vectorstore.similarity_search(query, k=k)
    if not docs:
        return ""
    # Combine content for CRAG/LLM ingestion
    return "\n".join([f"[{d.metadata.get('source', 'unknown')}] {d.page_content}" for d in docs])
