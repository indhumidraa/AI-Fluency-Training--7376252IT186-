import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load the existing repo-level .env file.
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_FILE)

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
BASE_URL = "https://api.groq.com/openai/v1"

if not API_KEY:
    raise SystemExit(
        f"GROQ_API_KEY was not found. Check your environment file: {ENV_FILE}"
    )

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = (
    "You are StudyBuddy, a concise and friendly AI study assistant. "
    "Explain concepts clearly and use a short example when helpful."
)


def non_streaming_demo():
    print("\n=== 1. NON-STREAMING RESPONSE ===")
    start = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "Explain recursion to a college student in 3 sentences.",
            },
        ],
        temperature=0.3,
        max_tokens=180,
    )

    elapsed = time.perf_counter() - start
    print(response.choices[0].message.content)
    print(f"Total request time: {elapsed:.3f} seconds")
    print(f"Model: {response.model}")


def streaming_demo():
    print("\n=== 2. STREAMING + PERFORMANCE ===")
    start = time.perf_counter()
    first_token_time = None
    chunks = []
    output_tokens = 0

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "Give 5 practical tips for preparing for a programming exam.",
            },
        ],
        temperature=0.3,
        max_tokens=250,
        stream=True,
        stream_options={"include_usage": True},
    )

    for chunk in stream:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                if first_token_time is None:
                    first_token_time = time.perf_counter() - start
                print(content, end="", flush=True)
                chunks.append(content)

        # Some compatible APIs send usage in a final chunk with no choices.
        if getattr(chunk, "usage", None):
            output_tokens = chunk.usage.completion_tokens or 0

    total_time = time.perf_counter() - start
    text = "".join(chunks)

    print("\n")
    print(f"Model: {MODEL}")
    print(f"Time to first content (TTFT): {first_token_time:.3f} seconds"
          if first_token_time is not None else "TTFT: unavailable")
    print(f"Total streaming time: {total_time:.3f} seconds")
    print(f"Reported output tokens: {output_tokens or 'not provided by API'}")

    if output_tokens and total_time > 0:
        print(f"Approx. output tokens/second (including request latency): "
              f"{output_tokens / total_time:.2f}")
    else:
        print("Tokens/second: unavailable because token usage was not reported.")
    print("Note: TTFT here measures time to first non-empty text chunk.")


def prompt_override_demo():
    print("\n=== 3. PROMPT OVERRIDE ===")
    custom_system_prompt = (
        "You are StudyBuddy in EXAM-REVISION mode. "
        "Answer in exactly 3 short bullet points and avoid long explanations."
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": custom_system_prompt},
            {
                "role": "user",
                "content": "How should I revise linked lists?",
            },
        ],
        temperature=0.2,
        max_tokens=150,
    )

    print("Override prompt:", custom_system_prompt)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    print("STUDYBUDDY - GROQ OPENAI-COMPATIBLE API DEMO")
    print("This tests a hosted API, not a local Ollama model.")
    non_streaming_demo()
    streaming_demo()
    prompt_override_demo()
