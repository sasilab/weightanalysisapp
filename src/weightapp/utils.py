# gripper_ranker/app/utils.py

import fitz  # PyMuPDF
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()  # Load .env values

# Create OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file_path: str) -> str:
    """Extract raw text from a PDF file using PyMuPDF."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_parameters(text: str) -> dict:
    """Use OpenAI to extract gripper parameters from research paper text."""
    prompt = f"""
Extract the following gripper parameters from the text below: 
- Actuation mechanism
- Payload capacity
- Gripping material
- Control algorithm
- Impact resistance

Return the result in **valid JSON format** with parameter names as keys and their values as strings. 
If not found, say "Not available" for that parameter.

TEXT:
\"\"\"
{text[:4000]}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        content = response.choices[0].message.content

        # Parse safely to dict
        parsed = json.loads(content)
        return parsed
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format from LLM"}
    except Exception as e:
        return {"error": str(e)}
