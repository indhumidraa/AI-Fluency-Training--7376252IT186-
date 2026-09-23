from collections import Counter

from config import client, MODEL


QUESTION = """
A college is organizing a technical workshop.

The total budget is Rs. 25,000.
Venue rental costs Rs. 8,000.
Food costs Rs. 7,500.
Promotional materials cost Rs. 3,500.

How much money remains after paying all three expenses?
"""


PROMPT = """
Solve the problem carefully step by step.

At the end, write exactly:

Final Answer: <answer>
"""


def ask(temperature):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "user",
                "content": QUESTION,
            },
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content.strip()


def extract_answer(text):

    for line in reversed(text.splitlines()):

        if "Final Answer:" in line:
            return line.split(
                "Final Answer:", 1
            )[1].strip()

    return text.splitlines()[-1].strip()


if __name__ == "__main__":

    print("=" * 70)
    print("SELF-CONSISTENCY")
    print("=" * 70)

    runs = 5

    print("\nQUESTION:")
    print(QUESTION)

    print("\nTemperature = 0.8")

    answers = []

    for i in range(runs):

        output = ask(0.8)
        answer = extract_answer(output)

        answers.append(answer)

        print(f"Run {i + 1}: {answer}")

    counts = Counter(answers)

    majority_answer, count = counts.most_common(1)[0]

    print("\nMajority Answer:")
    print(majority_answer)

    print(f"Count: {count}/{runs}")

    print("\nTemperature = 0")

    output = ask(0)

    print(output)