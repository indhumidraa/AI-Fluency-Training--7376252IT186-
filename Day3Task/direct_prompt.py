import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("../.env")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")


questions = [
    "What is a shopping bill?",
    "I bought 3 notebooks at Rs. 80 each and 2 pens at Rs. 20 each. What is the total bill?",
    "Why is it useful to keep a shopping bill?"
]


for i, question in enumerate(questions, 1):

    print("=" * 60)
    print(f"QUESTION {i}")
    print("=" * 60)

    print("Q:", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    print("\nLLM ANSWER:")
    print(answer)