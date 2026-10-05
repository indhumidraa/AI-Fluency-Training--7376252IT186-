# structured_outputs.py
# Compare unconstrained output, JSON mode, and schema-constrained output.

import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def create_client():
    if PROVIDER.lower() == "groq":
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is missing from .env")

        return OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

    raise RuntimeError(f"Unsupported provider: {PROVIDER}")


QUESTION = """
Extract the following student information:
Name: Ananya
Department: Information Technology
Year: 2
Skills: Python, SQL, Machine Learning
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "department": {
            "type": "string"
        },
        "year": {
            "type": "integer"
        },
        "skills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "name",
        "department",
        "year",
        "skills"
    ],
    "additionalProperties": False
}


def run_no_constraint(client):
    print("\n" + "=" * 70)
    print("1. NO CONSTRAINT")
    print("=" * 70)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract the student information clearly."
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        max_tokens=300
    )

    raw = response.choices[0].message.content

    print("Raw reply:")
    print(raw)

    try:
        parsed = json.loads(raw)
        print("\nParsed result:")
        print(json.dumps(parsed, indent=2))
    except Exception as exc:
        print(f"\nParsed result/error: {exc}")


def run_json_mode(client):
    print("\n" + "=" * 70)
    print("2. JSON MODE")
    print("=" * 70)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Return only valid JSON containing the fields "
                    "name, department, year, and skills."
                )
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        response_format={
            "type": "json_object"
        },
        max_tokens=300
    )

    raw = response.choices[0].message.content

    print("Raw reply:")
    print(raw)

    try:
        parsed = json.loads(raw)
        print("\nParsed result:")
        print(json.dumps(parsed, indent=2))
    except Exception as exc:
        print(f"\nParsed result/error: {exc}")


def run_schema_mode(client):
    print("\n" + "=" * 70)
    print("3. SCHEMA MODE")
    print("=" * 70)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Extract the student information."
                },
                {
                    "role": "user",
                    "content": QUESTION
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "student_information",
                    "strict": True,
                    "schema": SCHEMA
                }
            },
            max_tokens=300
        )

        raw = response.choices[0].message.content

        print("Raw reply:")
        print(raw)

        try:
            parsed = json.loads(raw)
            print("\nParsed result:")
            print(json.dumps(parsed, indent=2))
        except Exception as exc:
            print(f"\nParsed result/error: {exc}")

    except Exception as exc:
        print("\nSchema mode error:")
        print(exc)


if __name__ == "__main__":
    print("=" * 70)
    print("STRUCTURED OUTPUT COMPARISON")
    print("=" * 70)
    print(f"Provider: {PROVIDER}")
    print(f"Model: {MODEL}")

    try:
        client = create_client()

        run_no_constraint(client)
        run_json_mode(client)
        run_schema_mode(client)

    except Exception as exc:
        print("\nProgram error:")
        print(exc)