# agent.py
# Reliable Tool Calling Agent - College Study Planner

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import SCHEMAS, TOOL_FUNCTIONS
from validator import validate_json_arguments


load_dotenv()


PROVIDER = os.getenv("PROVIDER", "groq")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def create_client():
    """Create an OpenAI-compatible client."""

    if PROVIDER.lower() == "groq":
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is missing from .env")

        return OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

    raise RuntimeError(
        f"Unsupported provider: {PROVIDER}. "
        "Currently configured for Groq."
    )


def build_tool_definitions():
    """Build OpenAI-compatible tool definitions from SCHEMAS."""

    definitions = []

    for name, schema in SCHEMAS.items():
        definitions.append({
            "type": "function",
            "function": {
                "name": schema["name"],
                "description": schema["description"],
                "parameters": schema["parameters"],
                "strict": schema.get("strict", True)
            }
        })

    return definitions


def handle_tool_call(tool_call):
    """
    Handle one model-generated tool call safely.

    Stages:
    1. Parse JSON
    2. Look up tool
    3. Validate arguments
    4. Execute function
    """

    function_name = tool_call.function.name
    raw_arguments = tool_call.function.arguments

    # Stage 1: Parse JSON
    try:
        arguments = json.loads(raw_arguments)
    except json.JSONDecodeError as exc:
        return f"Tool error: invalid JSON: {exc}"

    # Stage 2: Look up tool
    if function_name not in TOOL_FUNCTIONS:
        return (
            f"Tool error: unknown tool '{function_name}'. "
            f"Available tools: {list(TOOL_FUNCTIONS.keys())}"
        )

    # Stage 3: Validate
    _, error = validate_json_arguments(
        function_name,
        raw_arguments
    )

    if error:
        return f"Tool error: {error}"

    # Stage 4: Execute
    try:
        result = TOOL_FUNCTIONS[function_name](**arguments)
        return str(result)
    except Exception as exc:
        return f"Tool error during execution: {exc}"


def run_agent(user_question, max_steps=6, max_tokens=300):
    """Run the reliable tool-calling loop."""

    client = create_client()
    tools = build_tool_definitions()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a reliable college study planner. "
                "Use the available tools when necessary. "
                "You may call multiple tools for one question. "
                "Never invent or silently change user-provided argument values. "
                "If the user provides a value that is not allowed by a tool schema, "
                "attempt the tool call with that value so the validator can reject it. "
                "If a tool reports an error, correct the call only when appropriate."
            )
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    previous_signature = None
    repeated_count = 0
    current_max_tokens = max_tokens

    for step in range(1, max_steps + 1):

        print(f"\n--- Step {step} ---")
        print(f"max_tokens = {current_max_tokens}")

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=True,
                max_tokens=current_max_tokens
            )
        except Exception as exc:
            print(f"API error: {exc}")
            return

        choice = response.choices[0]
        message = choice.message
        finish_reason = choice.finish_reason

        print(f"finish_reason = {finish_reason}")

        # Retry truncated responses with more tokens.
        if finish_reason == "length":
            print("Response truncated. Retrying with more tokens.")

            messages.append({
                "role": "assistant",
                "content": message.content or ""
            })

            current_max_tokens *= 2
            continue

        # Final normal response.
        if not message.tool_calls:
            print("\nFinal answer:")
            print(message.content)
            print(f"\nTotal steps: {step}")
            return

        # Save assistant tool-call message.
        messages.append(message)

        # Build a signature for repeated-call detection.
        signature = tuple(
            (
                call.function.name,
                call.function.arguments
            )
            for call in message.tool_calls
        )

        if signature == previous_signature:
            repeated_count += 1
        else:
            repeated_count = 0

        previous_signature = signature

        if repeated_count >= 2:
            print(
                "\nStopped: repeated identical tool calls detected."
            )
            return

        # Process EVERY tool call.
        print(
            f"Number of tool calls in this response: "
            f"{len(message.tool_calls)}"
        )

        for tool_call in message.tool_calls:

            print(
                f"\nTool call: {tool_call.function.name}"
            )

            print(
                f"Arguments: {tool_call.function.arguments}"
            )

            result = handle_tool_call(tool_call)

            print(f"Tool result: {result}")

            # One tool message for every tool_call_id.
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    print(
        f"\nStopped: maximum number of steps "
        f"({max_steps}) reached."
    )


if __name__ == "__main__":

    print("=" * 60)
    print("COLLEGE STUDY PLANNER - RELIABLE TOOL AGENT")
    print("=" * 60)

    questions = [
        # 1. Single tool
        "What is the difficulty and credit value of Data Structures?",

        # 2. Two tools / parallel tool-call opportunity
        (
            "Tell me the difficulty of Data Structures and calculate "
            "how many hours per day I should study if I have 5 days."
        ),

        # 3. Invalid enum temptation
        (
            "How many hours should I study for an extreme difficulty "
            "subject for 3 days?"
        ),

        # 4. No tool
        "What is a stack in data structures?"
    ]

    for number, question in enumerate(questions, start=1):

        print("\n" + "=" * 60)
        print(f"QUESTION {number}")
        print("=" * 60)
        print(question)

        run_agent(question)