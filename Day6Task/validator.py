# validator.py
# Validates model-generated tool arguments before a tool is executed.

import json
from tools import SCHEMAS


def validate_arguments(tool_name, arguments):
    """
    Validate tool arguments against the shared SCHEMAS dictionary.

    Returns:
        None if valid
        A descriptive error message if invalid
    """

    if tool_name not in SCHEMAS:
        return f"Unknown tool '{tool_name}'. Expected one of: {list(SCHEMAS.keys())}"

    schema = SCHEMAS[tool_name]["parameters"]

    if not isinstance(arguments, dict):
        return "Arguments must be a JSON object."

    # Check required arguments
    required = schema.get("required", [])

    for field in required:
        if field not in arguments:
            return (
                f"Missing required argument '{field}'. "
                f"Expected required fields: {required}"
            )

    # Check invented arguments
    allowed = schema.get("properties", {})

    if schema.get("additionalProperties") is False:
        extra = set(arguments.keys()) - set(allowed.keys())

        if extra:
            return (
                f"Invented argument(s): {sorted(extra)}. "
                f"Expected only: {list(allowed.keys())}"
            )

    # Check each argument
    for field, value in arguments.items():

        if field not in allowed:
            continue

        field_schema = allowed[field]
        expected_type = field_schema.get("type")

        # Type validation
        if expected_type == "string" and not isinstance(value, str):
            return (
                f"Wrong type for '{field}'. "
                f"Expected string, got {type(value).__name__}."
            )

        if expected_type == "integer":
            # bool is technically an int in Python, but it should not count.
            if isinstance(value, bool) or not isinstance(value, int):
                return (
                    f"Wrong type for '{field}'. "
                    f"Expected integer, got {type(value).__name__}."
                )

        if expected_type == "number":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return (
                    f"Wrong type for '{field}'. "
                    f"Expected number, got {type(value).__name__}."
                )

        # Enum validation
        if "enum" in field_schema:
            if value not in field_schema["enum"]:
                return (
                    f"Invalid value for '{field}': '{value}'. "
                    f"Expected one of: {field_schema['enum']}"
                )

    return None


def validate_json_arguments(tool_name, raw_arguments):
    """
    Parse a JSON argument string and validate it.

    Returns:
        (arguments, None) when valid
        (None, error_message) when invalid
    """

    try:
        arguments = json.loads(raw_arguments)
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON arguments: {exc}"

    error = validate_arguments(tool_name, arguments)

    if error:
        return None, error

    return arguments, None


if __name__ == "__main__":
    print("Validator self-test")
    print("=" * 50)

    tests = [
        (
            "Valid call",
            "calculate_study_hours",
            {"difficulty": "hard", "days": 5}
        ),
        (
            "Missing required argument",
            "calculate_study_hours",
            {"difficulty": "hard"}
        ),
        (
            "Invented extra argument",
            "calculate_study_hours",
            {
                "difficulty": "hard",
                "days": 5,
                "location": "college"
            }
        ),
        (
            "Wrong type",
            "calculate_study_hours",
            {
                "difficulty": "hard",
                "days": "five"
            }
        ),
        (
            "Invalid enum value",
            "calculate_study_hours",
            {
                "difficulty": "extreme",
                "days": 5
            }
        ),
        (
            "Unknown tool",
            "unknown_tool",
            {}
        )
    ]

    for name, tool, arguments in tests:
        error = validate_arguments(tool, arguments)

        print(f"\n{name}")
        print(f"Tool: {tool}")
        print(f"Arguments: {arguments}")
        print(f"Result: {'VALID' if error is None else error}")