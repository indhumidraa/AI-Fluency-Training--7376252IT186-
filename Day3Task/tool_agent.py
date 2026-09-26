import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("../.env")

from tool import calculate_bill


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_bill",
            "description": "Calculate the total price of shopping items using their price and quantity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "List of shopping items with name, price and quantity.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string"
                                },
                                "price": {
                                    "type": "number"
                                },
                                "quantity": {
                                    "type": "integer"
                                }
                            },
                            "required": ["name", "price", "quantity"]
                        }
                    }
                },
                "required": ["items"]
            }
        }
    }
]


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

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:

        for tool_call in message.tool_calls:

            print("\nTOOL CALL:")
            print("Tool:", tool_call.function.name)
            print("Arguments:", tool_call.function.arguments)

            arguments = json.loads(tool_call.function.arguments)

            result = calculate_bill(arguments["items"])

            print("TOOL RESULT:")
            print(result)

            messages.append(message)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            )

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        print("\nFINAL ANSWER:")
        print(final_response.choices[0].message.content)

    else:

        print("\nTOOL CALL:")
        print("No tool was needed.")

        print("\nFINAL ANSWER:")
        print(message.content)