# Day 6 Observations

## 1. Fault Injection Table

| Fault | Message returned | Run continued? |
|---|---|---|
| Invalid JSON | Invalid JSON arguments returned | Y |
| Unknown tool | Unknown tool error with available tools | Y |
| Missing required argument | Validation error for missing `course_code` | Y |
| Wrong type | Validation error: `course_code` must be a string | Y |
| Value outside enum | Validation error: semester must be `odd` or `even` | Y |
| Invented extra argument | Validation error for unexpected `year` | Y |
| Unsafe expression | Calculator rejected unsupported expression | Y |
| Case-insensitive tool name | Unknown tool error | Y |
| JSON array arguments | Arguments must be a JSON object | Y |

All deliberately malformed tool calls returned recoverable messages without crashing the program.

---

## 2. Agent Behavior

### Question 1

**Question:** What is the total fee for CS101 and AI202 after a 10% scholarship?

Observed tool sequence:

1. `get_course_fee(CS101)` → 12000
2. `get_course_fee(AI202)` → 18000
3. `calculator((12000+18000)*0.9)` → 27000

**Final answer:** ₹27,000.

### Question 2

**Question:** Is DS303 more expensive than CS101, and by how much?

Observed tool sequence:

1. `get_course_fee(DS303)` → 15000
2. `get_course_fee(CS101)` → 12000
3. `calculator(15000-12000)` → 3000

**Final answer:** DS303 is ₹3,000 more expensive than CS101.

### Question 3

**Question:** What is the fee for ME404?

The agent identified that ME404 is not a valid course code and returned the valid course codes instead of inventing a fee.

### Question 4

**Question:** Write a one-line welcome message for new AI students.

The agent answered directly without calling a tool because no fee or arithmetic operation was required.

---

## 3. Parallel Tool Calls

A direct test requesting fees for CS101 and AI202 returned:

- `finish_reason: tool_calls`
- `tool_calls: 1`
- Tool called: `get_course_fee` for CS101

The model chose sequential tool use rather than returning two parallel tool calls in this test.

However, `robust_agent.py` is implemented to process every tool call returned by the model and append one tool message for each `tool_call_id`.

---

## 4. finish_reason = length

A test using `max_tokens=5` produced:

```text
finish_reason: length