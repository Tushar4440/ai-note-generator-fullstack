import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
if(API_KEY is None):
    raise ValueError("API_KEY environment value not set")

def generate_notes(context, new_input):
    prompt = f"""
    Context: 
    {context}

    New input:
    {new_input}

    Task:
    Summarize the new input into exactly 6 point notes.
    - Each note should be a single clear sentence.
    - Keep them factual, short, and easy to skim.
    - Do not write essays, stories, or single words.
    """

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}'

    response = requests.post(
        url,
        json={
            "contents":[
                {"parts":
                    [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 500,
            }
        }
    )


    data = response.json()
    print(data['candidates'][0]['content']['parts'][0]['text'])
    return data['candidates'][0]['content']['parts'][0]['text']