import json
import requests
from rag_engine import retrieve_context


def generate_rag_explanation(activity_details):

    context = retrieve_context(
        "digital forensics suspicious login sensitive file USB activity"
    )

    url = "http://localhost:11434/api/generate"

    activity_text = json.dumps(activity_details, indent=2, default=str)

    prompt = f"""
You are a digital forensics assistant.

Analyze ONLY the events provided below.

Knowledge:
{context}

Actual Investigation Records:
{activity_text}

IMPORTANT RULES:
- Never invent events, users, files, timestamps, or actions.
- Mention each recorded event only once.
- Use exact timestamps from the records.
- Clearly distinguish recorded facts from observations.
- Do not calculate or invent time windows.
- Use only the timestamps and time differences shown in the records.
- USB connection does not prove file copying.
- Do not assume anyone is guilty.
- If information is missing, say "Not available in the records".
- Do not repeat sentences.

Write a short explanation using these headings:

RECORDED FACTS
TIMELINE ANALYSIS
INVESTIGATION OBSERVATIONS
LIMITATIONS
CONCLUSION

Use simple English. Keep each heading to 1 or 2 short sentences.
"""

    data = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False,
        "options": {
    "num_predict": 350,
    "temperature": 0.1,
    "num_ctx": 2048,
    "repeat_penalty": 1.2
    }
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=300
        )

        response.raise_for_status()
        result = response.json()["response"]

        result = result.replace("\\*", "")
        result = result.replace("*", "")

        return result

    except requests.RequestException as error:
        return f"AI connection error: {error}"


if __name__ == "__main__":

    sample_activity = """
    User demo logged in successfully.
    The same user accessed a sensitive file.
    A USB device was connected within 30 minutes.
    """

    print("Generating RAG-based AI explanation...")

    result = generate_rag_explanation(sample_activity)

    print("\nAI + RAG FORENSIC EXPLANATION\n")
    print(result)
