import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

def load_brand_voice(file_path="brand_voice.json"):
    """Loads brand voice configuration from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)

def generate_marketing_copy(product_description: str) -> dict:
    """Generates structured marketing copy using Google Gemini API based on brand voice."""
    brand_voice = load_brand_voice()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from environment variables!")

    client = genai.Client(api_key=api_key)

    brand_name = brand_voice.get('brand_name', 'TaskFlow Software')
    tone = brand_voice.get('tone', '')
    style = brand_voice.get('style', '')
    target_audience = brand_voice.get('target_audience', '')
    key_phrases = ', '.join(brand_voice.get('key_phrases', []))

    system_prompt = f"""
    You are an expert marketing copywriter for {brand_name}.
    
    Adhere strictly to the following brand voice guidelines:
    - Tone: {tone}
    - Style: {style}
    - Target Audience: {target_audience}
    - Key Phrases to consider: {key_phrases}

    You must output ONLY valid JSON format with exactly these keys:
    {{
      "headline": "A catchy headline",
      "tagline": "A memorable tagline",
      "body": "A persuasive short paragraph body copy"
    }}
    Do not include any Markdown formatting like ```json, just raw JSON.
    """

    user_prompt = f"Product Description: {product_description}"

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        temperature=0.7,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=config,
    )

    content = response.text.strip()
    
    # Parse and return JSON response
    return json.loads(content)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        description = sys.argv[1]
    else:
        description = "An AI-powered task management tool that automatically prioritizes daily software engineering workflows."

    print(f"\nGenerating marketing content for:\n\"{description}\"\n")
    try:
        result = generate_marketing_copy(description)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error generating copy: {e}")