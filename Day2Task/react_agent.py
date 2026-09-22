from config import client, MODEL
from tool import course_info

QUESTION = (
    "I want to know the duration of AI202. "
    "Then tell me whether CS101 and AI202 together "
    "would cost less than Rs. 30,000."
)

print("QUESTION:", QUESTION)
print("\n--- ReAct Trace ---")

# Thought
print("\nThought: I need the course information before answering.")

# Action
print("Action: course_info('AI202')")

# Observation
ai_info = course_info("AI202")
print("Observation:", ai_info)

# Action
print("\nAction: course_info('CS101')")

# Observation
cs_info = course_info("CS101")
print("Observation:", cs_info)

# Now ask the LLM to interpret the tool results
prompt = f"""
Answer the user's question using the tool results below.

User question:
{QUESTION}

Tool result for AI202:
{ai_info}

Tool result for CS101:
{cs_info}

Explain the result briefly and give the final answer.
"""

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are a ReAct-style assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

print("\nFinal Answer:")
print(response.choices[0].message.content)