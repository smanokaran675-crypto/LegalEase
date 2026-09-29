import os
from dotenv import load_dotenv
from google import genai

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE, override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def generate_legal_document(document_type, party_name, details):

    if not API_KEY:
        return "Gemini API key is not configured. Please add GEMINI_API_KEY to the .env file."

    try:
        client = genai.Client(api_key=API_KEY)

        prompt = f"""
Create a professional legal document draft.

Document Type: {document_type}
Party / Company Name: {party_name}
Additional Details: {details}

Use clear professional legal language.
Include suitable headings and clauses.
Make the document well structured and editable.
Do not invent personal information.
Mention that the document should be reviewed by a qualified legal professional.

Generate only the document.
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Unable to generate the document right now.\n\nError: {e}"