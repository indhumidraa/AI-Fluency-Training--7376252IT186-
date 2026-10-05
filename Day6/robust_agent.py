"""Day 6: robust function-calling agent with validation and retry."""

import json

from config import client, MODEL, banner
from tools_v2 import TOOLS, TOOL_FUNCTIONS, SCHEMAS
from validate import validate_arguments


SYSTEM_PROMPT = """You are a college fee assistant.

Rules:
1. Never guess a course fee.
2. Always call get_course_fee when a course fee is needed.
3. Use calculator for every arithmetic step.
4. Valid course codes are CS101, AI202, and DS303.
5. If no tool is needed, answer directly.
6. Keep answers concise.
"""

MAX_TOKENS = 500
REPEAT_LIMIT = 3


def handle_tool_call(call, log=True):
    """Safely execute one model-generated tool call."""
    name = call.function.name
    raw = call.function.arguments or "{}"

    # 1. Parse JSON arguments
    try:
        arguments = json.loads(raw)
    except json.JSONDecodeError as error:
        message = f"Invalid JSON arguments: {error}"
        if log:
            print("  TOOL ERROR:", message)
        return message

    # 2. Check whether the tool exists
    if name not in TOOL_FUNCTIONS:
        message = (
            f"Unknown tool '{name}'. "
            f"Available tools: {', '.join(TOOL_FUNCTIONS)}"
        )
        if log:
            print("  TOOL ERROR:", message)
        return message

    # 3. Validate arguments
    error = validate_arguments(arguments, SCHEMAS[name])
    if error:
        if log:
            print("  TOOL ERROR:", error)
        return f"Validation error: {error}"

    # 4. Execute the tool
    try:
        result = TOOL_FUNCTIONS[name](**arguments)
    except Exception as error:
        message = f"Tool execution error: {error}"
        if log:
            print("  TOOL ERROR:", message)
        return message

    if log:
        print(f"  TOOL: {name}({arguments}) -> {result}")

    return result


def agent(question, max_steps=6, verbose=True):
    """Run the robust tool-calling agent."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    seen = {}
    max_tokens = MAX_TOKENS

    for step in range(1, max_steps + 1):
        if verbose:
            print(f"\n--- Step {step} ---")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0,
            max_tokens=max_tokens,
        )

        choice = response.choices[0]
        message = choice.message
        finish_reason = choice.finish_reason

        # Handle truncation
        if finish_reason == "length":
            if max_tokens >= 2000:
                return "Stopped: response remained truncated."

            max_tokens *= 2

            if verbose:
                print(
                    f"  Response truncated. Retrying with "
                    f"max_tokens={max_tokens}"
                )

            continue

        # Final answer
        if not message.tool_calls:
            return message.content or "(No answer returned.)"

        # Add assistant tool-call message
        messages.append(message)

        # Execute every tool call
        for call in message.tool_calls:
            signature = (
                call.function.name,
                call.function.arguments or "{}",
            )

            seen[signature] = seen.get(signature, 0) + 1

            if seen[signature] >= REPEAT_LIMIT:
                return (
                    "Stopped: the same failing tool call was "
                    "repeated too many times."
                )

            result = handle_tool_call(call, log=verbose)

            # Exactly one tool message per tool call ID
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    return "Stopped: maximum agent steps reached."


if __name__ == "__main__":
    banner("Day 6 Robust Agent")

    questions = [
        "What is the total fee for CS101 and AI202 after a 10% scholarship?",
        "Is DS303 more expensive than CS101, and by how much?",
        "What is the fee for ME404?",
        "Write a one-line welcome message for new AI students.",
    ]

    for number, question in enumerate(questions, start=1):
        print(f"\n{'=' * 60}")
        print(f"QUESTION {number}: {question}")
        print("=" * 60)

        try:
            answer = agent(question)
            print("\nFINAL ANSWER:", answer)
        except Exception as error:
            print("\nAGENT ERROR:", error)