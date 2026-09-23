# Individual Conceptual Analysis – Reasoning and Acting

## 1. Scenario

A college is organizing a technical workshop with a budget of Rs. 25,000.

The expenses are:

- Venue rental: Rs. 8,000
- Food: Rs. 7,500
- Promotional materials: Rs. 3,500

The scenario is used to compare Direct Prompting, Chain-of-Thought (CoT), ReAct, and Self-Consistency.

The questions include simple calculations, multi-step reasoning, and a question requiring external information through a weather tool.

---

## 2. Direct Prompting

Direct prompting asks the model to provide an answer directly without displaying its reasoning or using an external tool.

For the workshop scenario, Direct Prompting was used to answer questions involving the budget and expenses.

### Observation

The model provided direct answers to the questions without showing intermediate reasoning.

### Advantages

- Simple to implement.
- Fast.
- Suitable for straightforward questions.
- Does not require additional tools.

### Limitation

Direct prompting cannot independently retrieve new external information through a tool.

---

## 3. Chain-of-Thought

Chain-of-Thought prompting asks the model to solve a problem step by step and show the important calculations.

### Observation

The model explained the calculations before giving the final answer.

For example, the remaining budget can be calculated as:

Total expenses = Rs. 8,000 + Rs. 7,500 + Rs. 3,500

Total expenses = Rs. 19,000

Remaining budget = Rs. 25,000 - Rs. 19,000

Remaining budget = Rs. 6,000

### Advantages

- Useful for multi-step reasoning.
- Makes calculations easier to follow.
- Helps organize the solution process.

### Limitation

CoT alone does not provide external information that requires a tool.

---

## 4. ReAct

ReAct combines reasoning with actions and observations from external tools.

The ReAct implementation used a weather tool to obtain current weather information for Chennai.

The process followed:

Thought → Action → Observation → Final Answer

### Observation

For the weather question, the agent selected the weather tool:

Action: get_current_weather

Action Input: Chennai

The tool returned:

Current weather in Chennai: 29.7°C, humidity 59%.

The agent then used this observation to provide the final answer.

### Advantages

- Can interact with external tools.
- Can obtain information that is not directly provided in the question.
- Combines reasoning with actions and observations.

### Limitation

It requires additional code for tool execution and error handling.

---

## 5. Self-Consistency

Self-Consistency was tested using the workshop budget calculation.

The Chain-of-Thought question was run multiple times with a non-zero temperature.

The generated answers were recorded and compared to identify the majority answer.

### Observation

The repeated runs produced answers that could be compared for consistency.

The majority answer was identified from the repeated results.

The same question was then run with temperature 0.

At temperature 0, the response was more deterministic compared with the non-zero-temperature runs.

### Purpose

Self-Consistency provides multiple reasoning attempts and uses agreement between the results as an additional way of checking an answer.

---

## 6. Comparison

| Aspect | Direct Prompting | Chain-of-Thought | ReAct |
|---|---|---|---|
| Reasoning depth | Direct | Step-by-step | Reasoning + actions |
| Tool usage | No | No | Yes |
| Multi-step questions | Suitable for simple problems | Suitable | Suitable |
| Transparency | Direct answer | Shows reasoning process | Shows action and observation process |
| Speed/cost | Generally lower | Generally higher | Generally higher because of tool interaction |
| Consistency | Usually high at low temperature | Can vary with temperature | Depends on reasoning and tool results |

---

## 7. Suitability

### Direct Prompting

Direct prompting is suitable for simple questions where the required information is already available in the prompt.

### Chain-of-Thought

Chain-of-Thought is suitable for questions requiring multiple reasoning or calculation steps.

### ReAct

ReAct is suitable when a task requires both reasoning and external information obtained through tools.

### Self-Consistency

Self-Consistency is suitable when repeated reasoning attempts can be compared to identify a consistent answer.

---

## 8. Conclusion

The experiment demonstrates that different prompting approaches are useful for different types of tasks.

Direct Prompting provides a simple and direct response. Chain-of-Thought provides a structured reasoning process for multi-step problems. ReAct extends reasoning by allowing interaction with an external tool. Self-Consistency compares multiple reasoning attempts to examine consistency.

The choice of approach depends on whether the task requires direct answering, multi-step reasoning, or external information.