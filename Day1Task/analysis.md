# Day 1 Task: Comparing a Plain Chatbot, Rule-Based Workflow, and AI Agent

## Scenario

The chosen scenario is course selection based on private course-price data.

The user asks:

> I can pay Rs. 30,000. Which two courses can I take together?

The course names and prices are stored privately in `expenses.txt`.

The three approaches are implemented as:

- `chatbot.py` – Plain Chatbot
- `workflow.py` – Rule-Based Workflow
- `agent.py` – AI Agent

---

# 1. Plain Chatbot

The plain chatbot uses an LLM to respond to the user's question.

In this implementation, the chatbot does not have access to the private `expenses.txt` file.

Therefore, it cannot determine the actual course combinations within the user's Rs. 30,000 budget.

The chatbot explains that it does not have access to the private course-price information.

### Characteristics

- Uses an LLM.
- Understands natural-language questions.
- Does not access the private course database/file.
- Does not use external tools.
- Does not perform the complete task using a tool-use loop.

### Limitation

The chatbot cannot reliably answer questions that depend on private data it cannot access.

---

# 2. Rule-Based Workflow

The rule-based workflow directly reads the private course-price data from `expenses.txt`.

It uses predefined programming rules to:

1. Read all courses and prices.
2. Generate every possible pair of courses.
3. Calculate the total price of each pair.
4. Check whether the total is less than or equal to Rs. 30,000.
5. Display the valid combinations.

The workflow does not use an LLM.

### Characteristics

- Uses predefined programming logic.
- Can access the private course-price file.
- Produces predictable results.
- Uses fixed conditions and steps.
- Does not dynamically decide which tools to use.

### Limitation

The workflow is less flexible because its process has to be explicitly programmed.

If the task changes significantly, the program may need new rules or code.

---

# 3. AI Agent

The AI agent combines:

**LLM + Tools + Loop**

The agent receives the user's question and decides which tools are required.

In this implementation, the agent has two tools:

### Tool 1: `read_course_data`

This tool reads the private course and price information from `expenses.txt`.

### Tool 2: `find_course_combinations`

This tool calculates which pairs of courses fit within the specified budget.

The agent can:

1. Understand the user's request.
2. Select an appropriate tool.
3. Execute the tool.
4. Observe the tool result.
5. Continue using another tool if required.
6. Generate the final response.

In the test run, the agent first used:

`read_course_data`

and then used:

`find_course_combinations`

It then returned the valid course combinations to the user.

### Characteristics

- Uses an LLM.
- Uses tools to access private data.
- Can perform multiple steps.
- Dynamically selects tools.
- Uses a loop until it has enough information to answer.
- Combines language understanding with programmatic actions.

---

# 4. Comparison

| Basis | Plain Chatbot | Rule-Based Workflow | AI Agent |
|---|---|---|---|
| Flexibility | High for conversation | Limited by predefined rules | High |
| Decision-making | LLM generates response | Fixed programming conditions | LLM selects tools |
| Tool usage | No tools | Direct program logic | Uses tools |
| Private-data access | No | Yes | Yes through tools |
| Multi-step task handling | Limited | Fixed steps | Dynamic loop |
| Automation | Limited | High for fixed tasks | High |
| Reliability | Limited when private data is required | Predictable for defined rules | Depends on tools and agent behavior |

---

# 5. Suitability Analysis

## Plain Chatbot

The plain chatbot is suitable for general conversational questions where private data or external actions are not required.

For this scenario, it cannot provide the actual course combinations because it does not have access to the private course-price data.

## Rule-Based Workflow

The rule-based workflow is suitable when the task is predictable and the required steps can be explicitly defined.

For this scenario, it can reliably calculate course combinations because the budget comparison rules are clearly defined.

## AI Agent

The AI agent is suitable when a task requires flexible decision-making, private-data access through tools, and multiple steps.

For this scenario, the agent can understand the request, select tools, access private data, calculate combinations, observe the results, and provide a final response.

---

# 6. Conclusion

The three approaches solve the problem in different ways.

A **plain chatbot** mainly generates a response using an LLM but cannot access the private course-price data.

A **rule-based workflow** directly follows predefined programming rules and can reliably process the private data.

An **AI agent** combines an LLM with tools and a loop. It can decide which tools to use, observe their results, and continue through multiple steps before producing the final response.

Therefore, the main distinction is:

> **Chatbot = LLM response**

> **Workflow = predefined rules**

> **Agent = LLM + Tools + Loop**