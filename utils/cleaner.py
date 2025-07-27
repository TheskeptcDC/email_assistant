import re

def clean_text(text):
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'(?i)(unsubscribe|privacy policy|terms of service|view in browser|click here).*', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()
