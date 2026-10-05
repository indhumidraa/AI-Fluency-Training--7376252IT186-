"""Day 6: compare unconstrained, JSON mode, and strict JSON schema."""

import json

from config import client, MODEL, banner


SCHEMA = {
    "type": "object",
    "properties": {
        "course_code": {
            "type": "string",
        },
        "wants_scholarship": {
            "type": "boolean",
        },
        "needs_tool": {
            "type": "boolean",
        },
    },
    "required": [
        "course_code",
        "wants_scholarship",
        "needs_tool",
    ],
    "additionalProperties": False,
}

QUESTION = "What do I pay for AI202 if I have the merit scholarship?"


def ask(response_format, label):
    print(f"\n{'=' * 60}")
    print(label)
    print("=" * 60)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract the user's request as JSON. "
                        "Do not calculate the fee."
                    ),
                },
                {
                    "role": "user",
                    "content": QUESTION,
                },
            ],
            temperature=0,
            response_format=response_format,
            max_tokens=200,
        )

        raw = response.choices[0].message.content

        print("Raw:")
        print(raw)

        try:
            parsed = json.loads(raw)
            print("\nParsed:")
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError as error:
            print("\nJSON parse error:", error)

    except Exception as error:
        print("\nProvider/model error:")
        print(error)


if __name__ == "__main__":
    banner("Day 6 Structured Output Demo")

    # 1. No output constraint
    ask(None, "1. No constraint")

    # 2. JSON mode
    ask(
        {"type": "json_object"},
        "2. JSON mode",
    )

    # 3. Strict JSON schema
    ask(
        {
            "type": "json_schema",
            "json_schema": {
                "name": "fee_query",
                "schema": SCHEMA,
                "strict": True,
            },
        },
        "3. Strict JSON schema",
    )