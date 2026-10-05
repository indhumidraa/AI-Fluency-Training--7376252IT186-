"""Validation for model-generated tool arguments."""

from tools_v2 import SCHEMAS

TYPES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def validate_arguments(arguments, schema):
    """Return an error message if arguments violate the schema."""
    if not isinstance(arguments, dict):
        return "Arguments must be a JSON object."

    # Check required arguments
    for name in schema.get("required", []):
        if name not in arguments:
            expected = schema["properties"][name].get("type", "value")
            return (
                f"Missing required argument '{name}'. "
                f"Expected: {expected}."
            )

    # Check unexpected arguments
    if schema.get("additionalProperties") is False:
        extras = [
            key for key in arguments
            if key not in schema.get("properties", {})
        ]
        if extras:
            allowed = ", ".join(schema.get("properties", {}))
            return (
                f"Unexpected argument(s): {', '.join(extras)}. "
                f"Allowed: {allowed}."
            )

    # Check types and enum values
    for name, value in arguments.items():
        if name not in schema.get("properties", {}):
            continue

        rules = schema["properties"][name]
        expected_type = rules.get("type")

        if expected_type in TYPES:
            expected_python_type = TYPES[expected_type]

            if not isinstance(value, expected_python_type):
                return (
                    f"Argument '{name}' must be a {expected_type}, "
                    f"but got {type(value).__name__}: {value}"
                )

        if "enum" in rules and value not in rules["enum"]:
            allowed = ", ".join(map(str, rules["enum"]))
            return (
                f"Argument '{name}' must be one of {allowed}, "
                f"got {value}"
            )

    return None


if __name__ == "__main__":
    test_schema = SCHEMAS["get_course_fee"]

    tests = [
        {"course_code": "CS101"},
        {},
        {"course_code": 123},
        {"course_code": "CS101", "semester": "summer"},
        {"course_code": "CS101", "year": 2026},
        ["CS101"],
    ]

    for i, arguments in enumerate(tests, start=1):
        result = validate_arguments(arguments, test_schema)
        print(f"Test {i}: {result}")