from config import client, MODEL

QUESTION = (
    "A student has a budget of Rs. 30,000. "
    "CS101 costs Rs. 12,000, AI202 costs Rs. 18,000, "
    "and ML303 costs Rs. 15,000. "
    "Which two courses can the student take together?"
)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Answer directly. Do not use tools."
            )
        },
        {
            "role": "user",
            "content": QUESTION
        }
    ],
    temperature=0
)

print("QUESTION:")
print(QUESTION)

print("\nDIRECT PROMPTING ANSWER:")
print(response.choices[0].message.content)