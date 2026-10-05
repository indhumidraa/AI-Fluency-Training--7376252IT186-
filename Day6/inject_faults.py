"""Day 6: deliberately inject malformed tool calls."""

from robust_agent import handle_tool_call


class FakeFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class FakeCall:
    def __init__(self, name, arguments):
        self.function = FakeFunction(name, arguments)
        self.id = "fake-call"


FAULTS = [
    (
        "Good call",
        FakeCall("get_course_fee", '{"course_code": "CS101"}'),
    ),
    (
        "Invalid JSON",
        FakeCall("get_course_fee", '{"course_code": "CS101"'),
    ),
    (
        "Unknown tool",
        FakeCall("send_email", '{"to": "student@example.com"}'),
    ),
    (
        "Missing required argument",
        FakeCall("get_course_fee", '{"semester": "odd"}'),
    ),
    (
        "Wrong type",
        FakeCall("get_course_fee", '{"course_code": 101}'),
    ),
    (
        "Invalid enum",
        FakeCall(
            "get_course_fee",
            '{"course_code": "CS101", "semester": "summer"}',
        ),
    ),
    (
        "Invented extra argument",
        FakeCall(
            "get_course_fee",
            '{"course_code": "CS101", "year": 2026}',
        ),
    ),
    (
        "Unknown course",
        FakeCall("get_course_fee", '{"course_code": "ME404"}'),
    ),
    (
        "Unsafe expression",
        FakeCall(
            "calculator",
            """{"expression": "__import__('os').system('ls')"}""",
        ),
    ),
    (
        "Empty arguments",
        FakeCall("calculator", ""),
    ),
    (
        "Own fault 1 - case-insensitive tool name",
        FakeCall("GET_COURSE_FEE", '{"course_code": "CS101"}'),
    ),
    (
        "Own fault 2 - JSON array arguments",
        FakeCall("get_course_fee", '["CS101"]'),
    ),
]


if __name__ == "__main__":
    print("=" * 65)
    print("DAY 6 FAULT INJECTION TEST")
    print("=" * 65)

    for label, call in FAULTS:
        print(f"\n[{label}]")

        try:
            result = handle_tool_call(call, log=False)
            print("Result:", str(result)[:120])
            print("Status: CONTINUED")
        except Exception as error:
            print("EXCEPTION:", error)
            print("Status: CRASHED")