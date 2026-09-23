from config import client, MODEL


QUESTIONS = [
    (
        "A college is organizing a technical workshop. "
        "The budget is Rs. 25,000. Venue rental costs Rs. 8,000, "
        "food costs Rs. 7,500, and promotional materials cost Rs. 3,500. "
        "How much money remains after paying these expenses?"
    ),
    (
        "A technical workshop has 100 students attending. "
        "Each food package costs Rs. 75. "
        "What is the total food cost?"
    ),
    (
        "A college workshop has a budget of Rs. 25,000. "
        "Venue costs Rs. 8,000, food costs Rs. 7,500, "
        "and promotional materials cost Rs. 3,500. "
        "Can the organizer afford an additional equipment cost of Rs. 5,000?"
    ),
]


def ask(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Answer the question directly. "
                    "Do not show your reasoning."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("=" * 70)
    print("DIRECT PROMPTING")
    print("=" * 70)

    for number, question in enumerate(QUESTIONS, 1):
        print(f"\nQUESTION {number}:")
        print(question)

        print("\nANSWER:")
        print(ask(question))