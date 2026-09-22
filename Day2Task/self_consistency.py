from collections import Counter
from config import client, MODEL

QUESTION = (
    "A student has a budget of Rs. 30,000. "
    "CS101 costs Rs. 12,000, AI202 costs Rs. 18,000, "
    "and ML303 costs Rs. 15,000. "
    "Which two courses can the student take together?"
)

RUNS = 5
TEMPERATURE = 0.8

answers = []

for i in range(RUNS):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Solve the problem step by step and give "
                    "a clear final answer."
                )
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        temperature=TEMPERATURE
    )

    answer = response.choices[0].message.content.strip()

    print(f"\n--- RUN {i + 1} ---")
    print(answer)

    answers.append(answer)

counts = Counter(answers)

print("\n--- SELF-CONSISTENCY RESULT ---")

for answer, count in counts.most_common():
    print(f"{count} occurrence(s): {answer}")

winner, count = counts.most_common(1)[0]

print("\nMAJORITY ANSWER:")
print(winner)

print(f"\nMajority count: {count}/{RUNS}")