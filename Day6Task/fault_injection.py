# fault_injection.py
# Deliberately broken tool calls for testing reliability guards.
# No model or internet connection is used.

from types import SimpleNamespace
from agent import handle_tool_call


def make_call(tool_name, arguments):
    return SimpleNamespace(
        id="fault-test-id",
        function=SimpleNamespace(
            name=tool_name,
            arguments=arguments
        )
    )


faults = [
    (
        "1. Invalid JSON",
        make_call(
            "calculate_study_hours",
            '{"difficulty": "hard", "days": }'
        )
    ),
    (
        "2. Unknown tool",
        make_call(
            "delete_student_records",
            '{"subject": "Data Structures"}'
        )
    ),
    (
        "3. Missing required argument",
        make_call(
            "calculate_study_hours",
            '{"difficulty": "hard"}'
        )
    ),
    (
        "4. Wrong type",
        make_call(
            "calculate_study_hours",
            '{"difficulty": "hard", "days": "five"}'
        )
    ),
    (
        "5. Enum violation",
        make_call(
            "calculate_study_hours",
            '{"difficulty": "extreme", "days": 5}'
        )
    ),
    (
        "6. Invented argument",
        make_call(
            "calculate_study_hours",
            '{"difficulty": "hard", "days": 5, "location": "college"}'
        )
    ),
    (
        "7. Negative days",
        make_call(
            "calculate_study_hours",
            '{"difficulty": "hard", "days": -3}'
        )
    ),
    (
        "8. Null argument",
        make_call(
            "get_subject_info",
            '{"subject": null}'
        )
    ),
    (
        "9. Wrong argument structure",
        make_call(
            "get_subject_info",
            '["Data Structures"]'
        )
    ),
    (
        "10. Empty argument object",
        make_call(
            "calculate_study_hours",
            '{}'
        )
    )
]


if __name__ == "__main__":
    print("=" * 70)
    print("FAULT INJECTION TEST")
    print("No model or internet connection is used.")
    print("=" * 70)

    for title, fake_call in faults:
        print("\n" + "-" * 70)
        print(title)

        result = handle_tool_call(fake_call)

        print(f"Returned message: {result}")
        print("Run continued: YES")

    print("\n" + "=" * 70)
    print("FAULT INJECTION COMPLETE")
    print("=" * 70)