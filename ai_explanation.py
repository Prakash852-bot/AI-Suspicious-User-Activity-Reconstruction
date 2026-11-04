import requests


def generate_ai_explanation(activity_details):

    url = "http://localhost:11434/api/generate"

    prompt = f"""
    You are a digital forensics assistant.

    Analyze the following activity:

    {activity_details}

    Explain the activity in simple English.
    Do not invent evidence or assume the user is guilty.
    Mention that suspicious activity is not proof of wrongdoing.
    """

    data = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=120
        )

        response.raise_for_status()
        return response.json()["response"]

    except requests.RequestException as error:
        return f"Connection error: {error}"


if __name__ == "__main__":

    sample = """
    User demo logged in successfully.
    The same user accessed a sensitive file.
    A USB device was connected within 30 minutes.
    """

    result = generate_ai_explanation(sample)

    print("\nAI FORENSIC EXPLANATION\n")
    print(result)