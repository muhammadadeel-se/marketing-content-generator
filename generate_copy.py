import os
import json
import sys
import re
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


def load_brand_voice() -> dict:
    """Loads brand voice configuration from JSON file."""
    brand_file = os.path.join(os.path.dirname(__file__), "brand_voice.json")
    try:
        with open(brand_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "brand_name": "TaskFlow Software",
            "tone": "Professional, energetic, and clear",
            "style": "Concise, benefit-focused, modern",
            "key_phrases": [
                "Streamline your workflow",
                "Boost team productivity",
                "Smart automation made simple",
            ],
        }


def _build_fallback_copy(product_description: str, brand_voice: dict) -> dict:
    """Generates a local fallback response when the AI API is unavailable."""
    description = str(product_description or "").strip()
    brand_name = brand_voice.get("brand_name") or brand_voice.get("company_name") or "TaskFlow Software"
    key_phrases = brand_voice.get("key_phrases") or [
        "Streamline your workflow",
        "Boost team productivity",
        "Smart automation made simple",
    ]
    tagline = key_phrases[0] if key_phrases else "Streamline your workflow"

    normalized = re.sub(r"[^a-zA-Z0-9\s]", " ", description)
    words = [word.lower() for word in normalized.split() if len(word) > 3 and word.lower() not in {"with", "that", "from", "your", "into", "this", "they", "team", "teams", "for", "using", "tool", "software"}]
    focus = " ".join(words[:4]) or "workflow efficiency"

    headline = f"{brand_name} turns {focus} into momentum"
    body = (
        f"{description or 'Built for growing teams'} helps teams move faster, reduce friction, and deliver "
        f"with more confidence. {brand_name} keeps work clear, focused, and ready to scale."
    )

    return {
        "headline": headline,
        "tagline": tagline,
        "body": body,
    }


def generate_marketing_copy(product_description: str) -> dict:
    """Generates structured marketing copy using the OpenAI API, with a safe local fallback."""
    brand_voice = load_brand_voice()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return _build_fallback_copy(product_description, brand_voice)

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are a professional copywriter for {brand_voice.get('brand_name') or brand_voice.get('company_name', 'TaskFlow Software')}.

    Brand Guidelines:
    - Tone: {brand_voice.get('tone')}
    - Style: {brand_voice.get('style')}
    - Key Phrases to include or align with: {', '.join(brand_voice.get('key_phrases', []))}

    Task:
    Generate marketing copy for the following product description:
    "{product_description}"

    Output Requirements:
    Return ONLY a valid JSON object with the following keys:
    - "headline": A compelling title.
    - "tagline": A catchy one-liner.
    - "body": A short promotional paragraph.

    Do not include markdown formatting or extra text outside the JSON object.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert marketing copywriter that outputs strict JSON."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)
        if isinstance(parsed, dict) and {"headline", "tagline", "body"}.issubset(parsed):
            return parsed
    except Exception:
        pass

    return _build_fallback_copy(product_description, brand_voice)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        description = sys.argv[1]
    else:
        description = "An automated workflow management tool for modern software engineering teams."

    try:
        result = generate_marketing_copy(description)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error generating copy: {e}", file=sys.stderr)
        sys.exit(1)