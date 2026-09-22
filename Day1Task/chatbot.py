import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

QUESTION = (
    "I can pay Rs. 30,000. "
    "Which two courses can I take together?"
)

SYSTEM_PROMPT = """
You are a plain chatbot.

You can answer using your language-model knowledge.

You DO NOT have access to the user's private course-price data.

If the user asks about private course prices,
explain that you cannot access the private data.
"""

response = client.responses.create(
    model="openai/gpt-oss-20b",
    instructions=SYSTEM_PROMPT,
    input=QUESTION
)

print("Q:", QUESTION)
print("\nChatbot:")
print(response.output_text)