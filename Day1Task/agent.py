import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# -----------------------------
# TOOL 1: Read private data
# -----------------------------
def read_course_data():
    courses = []

    with open("expenses.txt", "r") as file:
        for line in file:
            name, price = line.strip().split(",")

            courses.append({
                "name": name.strip(),
                "price": int(price.strip())
            })

    return courses


# -----------------------------
# TOOL 2: Find course pairs
# -----------------------------
def find_course_combinations(budget):
    courses = read_course_data()

    combinations = []

    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):

            total = courses[i]["price"] + courses[j]["price"]

            if total <= budget:
                combinations.append({
                    "course1": courses[i]["name"],
                    "course2": courses[j]["name"],
                    "total": total
                })

    return combinations


# -----------------------------
# TOOLS
# -----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_course_data",
            "description": "Read the user's private course and price data.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_course_combinations",
            "description": "Find pairs of courses that fit within a budget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "budget": {
                        "type": "number",
                        "description": "Maximum budget available."
                    }
                },
                "required": ["budget"]
            }
        }
    }
]


QUESTION = (
    "I can pay Rs. 30,000. "
    "Which two courses can I take together?"
)


SYSTEM_PROMPT = """
You are an AI agent.

The user's course prices are private data.

You have tools that can access this private data.

Your job is to:

1. Understand the user's request.
2. Decide which tool is needed.
3. Use the tool.
4. Observe the result.
5. Give a clear final answer.

Never invent course prices.
"""


def agent(question):

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    # -----------------------------
    # AGENT LOOP
    # -----------------------------
    while True:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                *messages
            ],
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Convert assistant message to normal dictionary
        assistant_message = {
            "role": "assistant",
            "content": message.content
        }

        if message.tool_calls:
            assistant_message["tool_calls"] = []

            for tool_call in message.tool_calls:
                assistant_message["tool_calls"].append({
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                })

        messages.append(assistant_message)

        # -----------------------------
        # No tool call = final answer
        # -----------------------------
        if not message.tool_calls:
            return message.content

        # -----------------------------
        # Execute selected tools
        # -----------------------------
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print("\n[AGENT TOOL USED]")
            print(tool_name)

            if tool_name == "read_course_data":

                result = read_course_data()

            elif tool_name == "find_course_combinations":

                budget = arguments["budget"]
                result = find_course_combinations(budget)

            else:

                result = {
                    "error": "Unknown tool"
                }

            print("\n[TOOL RESULT]")
            print(result)

            # Send result back to agent
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })


# -----------------------------
# RUN AGENT
# -----------------------------

print("Q:", QUESTION)
print("\nAgent:")

answer = agent(QUESTION)

print(answer)