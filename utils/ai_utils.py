from google import genai
import os

def get_ai_response(question):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=f"Give one word answer {question}"
        )
        print(response.text)
        return response.text
    except Exception as e:
        print(e)
        return "Error", e