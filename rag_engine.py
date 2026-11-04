import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge_base" / "digital_forensics_basics.txt"
DB_PATH = BASE_DIR / "database" / "chroma_db"

# Lazy load embedding model
model = None

def get_embedding_model():
    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model
# Create ChromaDB storage
client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="digital_forensics_knowledge"
)


def load_knowledge():

    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {KNOWLEDGE_FILE}"
        )

    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    # Split text into paragraphs
    chunks = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    if not chunks:
        raise ValueError("Knowledge-base file is empty.")

    embeddings = model.encode(chunks).tolist()

    ids = [f"forensic_doc_{i}" for i in range(len(chunks))]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print(f"Stored {len(chunks)} knowledge sections.")


def retrieve_context(query, top_k=3):

    embedding_model = get_embedding_model()

    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count())
    )

    documents = results.get("documents", [[]])[0]

    return "\n\n".join(documents)


if __name__ == "__main__":

    load_knowledge()

    question = "What is digital evidence integrity?"

    context = retrieve_context(question)

    print("\nRetrieved Forensic Knowledge:\n")
    print(context)