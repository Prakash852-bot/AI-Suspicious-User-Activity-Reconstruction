
import re
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge_base" / "digital_forensics_basics.txt"

# Store knowledge paragraphs in memory
knowledge_chunks = []


def load_knowledge():

    global knowledge_chunks

    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {KNOWLEDGE_FILE}"
        )

    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    knowledge_chunks = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    if not knowledge_chunks:
        raise ValueError("Knowledge-base file is empty.")

    print(f"Loaded {len(knowledge_chunks)} knowledge sections.")

    return knowledge_chunks


def tokenize(text):

    return set(
        re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    )


def retrieve_context(query, top_k=3):

    global knowledge_chunks

    if not knowledge_chunks:
        load_knowledge()

    query_words = tokenize(query)

    if not query_words:
        return "\n\n".join(knowledge_chunks[:top_k])

    scored_chunks = []

    for paragraph in knowledge_chunks:

        paragraph_words = tokenize(paragraph)

        # Count matching keywords
        score = len(query_words.intersection(paragraph_words))

        if query.lower() in paragraph.lower():
            score += 5

        if score > 0:
            scored_chunks.append((score, paragraph))

    # Sort by relevance
    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    results = [
        paragraph
        for score, paragraph in scored_chunks[:top_k]
    ]

    if not results:
        return "\n\n".join(knowledge_chunks[:top_k])

    return "\n\n".join(results)


if __name__ == "__main__":

    load_knowledge()

    question = "What is digital evidence integrity?"

    context = retrieve_context(question)

    print("\nRetrieved Forensic Knowledge:\n")
    print(context)
