
"""Day 8: Agentic RAG college helpdesk."""

import ast
import operator

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from lc_config import get_model, get_vectorstore


COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000,
}

MAX_DISTANCE = 0.3
store = get_vectorstore()


@tool
def search_handbook(query: str) -> str:
    """Search college handbook documents for relevant policies."""
    results = store.similarity_search_with_score(query, k=3)
    relevant = [
        (doc, score)
        for doc, score in results
        if score <= MAX_DISTANCE
    ]

    if not relevant:
        return "NO_MATCH: The handbook does not contain a supported answer."

    return "\n\n".join(
        f"[{doc.metadata.get('source', 'unknown')}] {doc.page_content}"
        for doc, score in relevant
    )


@tool
def get_course_fee(course_code: str) -> str:
    """Get the fee for CS101, AI202, or DS303."""
    code = course_code.strip().upper()
    fee = COURSE_FEES.get(code)
    if fee is None:
        return f"Unknown course code: {code}"
    return f"{code} fee is Rs. {fee}"


@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check exam eligibility using attendance percentage."""
    if not 0 <= attendance_percent <= 100:
        return "Invalid attendance percentage."

    if attendance_percent >= 75:
        return f"Eligible with {attendance_percent}% attendance."

    if attendance_percent >= 65:
        return (
            f"Attendance is {attendance_percent}%. Below the usual 75% "
            "threshold; condonation may apply. Check official regulations."
        )

    return (
        f"Not eligible with {attendance_percent}% attendance. "
        "The minimum attendance requirement is 65%."
    )


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


@tool
def calculator(expression: str) -> str:
    """Calculate basic arithmetic with +, -, *, and /."""
    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        raise ValueError("Only basic arithmetic is supported.")

    try:
        return str(evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculation error: {error}"


tools = [
    search_handbook,
    get_course_fee,
    calculator,
    check_exam_eligibility,
]

SYSTEM = """
You are the Greenfield College helpdesk assistant.
Use search_handbook for college rules and policies.
Use get_course_fee for course fees.
Use calculator for arithmetic.
Use check_exam_eligibility for attendance questions.
If the handbook returns NO_MATCH, say the answer is not available
in the handbook. Never invent policies or fees.
Answer briefly and mention the source document when available.
"""

model = get_model().bind_tools(tools)


def agent(state: MessagesState):
    response = model.invoke([("system", SYSTEM)] + state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
graph = builder.compile(checkpointer=InMemorySaver())


def ask(question: str, thread_id: str = "student-1"):
    print(f"\nUSER: {question}")
    try:
        result = graph.invoke(
            {"messages": [HumanMessage(content=question)]},
            {"configurable": {"thread_id": thread_id}},
        )
        answer = result["messages"][-1].content
        print("ASSISTANT:", answer)
        return answer
    except Exception as error:
        print(f"AGENT ERROR: {type(error).__name__}: {error}")
        return None


def direct_tool_checks():
    print("\n" + "=" * 55)
    print("DIRECT TOOL VALIDATION")
    print("=" * 55)

    print(get_course_fee.invoke({"course_code": "CS101"}))
    print(get_course_fee.invoke({"course_code": "AI202"}))
    print("Arithmetic check:", calculator.invoke({
        "expression": "12000 + 18000 + 2000"
    }))
    print("Attendance check:", check_exam_eligibility.invoke({
        "attendance_percent": 70
    }))
    print(
        "Note: The Rs. 2,000 late fee in the arithmetic check is an "
        "assumption. Verify the actual maximum in fee_policy.md."
    )


if __name__ == "__main__":
    print("=" * 55)
    print("DAY 8 - AGENTIC RAG HELPDESK")
    print("MAX_DISTANCE:", MAX_DISTANCE)
    print("=" * 55)

    questions = [
        "What is the minimum CGPA required for placement?",
        "Can a student with 70% attendance write the exam?",
        "What is the CS101 course fee?",
        "What is the total of the CS101 fee, AI202 fee, and maximum late fee?",
        "What is the capital of France? Answer only if the college handbook supports it.",
    ]

    for question in questions:
        ask(question)

    direct_tool_checks()