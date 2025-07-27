import requests

SUMMARY_API_URL = "http://127.0.0.1:8000/summarize"

def summarize_content(email_text):
    payload = {
        "content": email_text,
        "model": "llama3.2"
    }
    try:
        response = requests.post(SUMMARY_API_URL, json=payload)
        return response.json().get("response", "No summary generated.")
    except Exception as e:
        return f"Error: {str(e)}"
