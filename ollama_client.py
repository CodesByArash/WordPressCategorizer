import requests
import json

def get_category_from_ollama(text):
    """Get category suggestion from Ollama"""
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": f"Suggest an appropriate English category name for the following blog post content:\n\n{text}\n\nOnly return the category name, nothing else."
    })
    for line in r.iter_lines():
        print(line)
        if line:
            data = json.loads(line)
            if 'response' in data:
                return data['response'].strip()
    return "Uncategorized" 