from config import client, MODEL
from tool import get_current_weather


def react(question, needs_weather=False, city="Chennai"):

    print("\n--- STEP 1 ---")
    print("Thought: I will determine whether external information is required.")

    if needs_weather:
        print("Action: get_current_weather")
        print(f"Action Input: {city}")

        try:
            observation = get_current_weather(city)
        except Exception as error:
            observation = f"Tool error: {error}"

        print(f"Observation: {observation}")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Use the provided tool observation to answer the question. "
                    "Do not call any tools. "
                    "Give only the final answer."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Tool Observation: {observation}"
                ),
            },
        ]

    else:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Solve the problem and give the final answer. "
                    "Do not call any tools."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )

    answer = response.choices[0].message.content.strip()

    print("\n--- FINAL ANSWER ---")
    print(answer)

    return answer


if __name__ == "__main__":

    print("=" * 70)
    print("REACT AGENT")
    print("=" * 70)

    question1 = (
        "A college is organizing a technical workshop. "
        "The budget is Rs. 25,000. Venue rental costs Rs. 8,000, "
        "food costs Rs. 7,500, and promotional materials cost "
        "Rs. 3,500. How much money remains after these expenses?"
    )

    print("\nQUESTION 1:")
    print(question1)

    react(question1)

    question2 = (
        "The technical workshop is being held in Chennai. "
        "What is the current weather in Chennai?"
    )

    print("\nQUESTION 2:")
    print(question2)

    react(question2, needs_weather=True, city="Chennai")