\# Day 2 Task – Reasoning and Acting



\## 1. Scenario



A student has a budget of Rs. 30,000. The available courses are:



\- CS101 – Rs. 12,000

\- AI202 – Rs. 18,000

\- ML303 – Rs. 15,000



The task compares Direct Prompting, Chain-of-Thought (CoT), and ReAct approaches for answering questions about the scenario.



\---



\## 2. Direct Prompting



Direct prompting asks the model to answer the question immediately without showing its reasoning or using external tools.



\### Observation



The model directly provided an answer based on the information included in the prompt.



\### Advantages



\- Simple to implement.

\- Fast response.

\- No external tool is required.

\- Suitable for straightforward questions.



\### Limitation



The model cannot obtain information that is not available in its prompt or existing knowledge.



\---



\## 3. Chain-of-Thought



Chain-of-Thought prompting asks the model to solve the problem step by step.



\### Observation



The model performed the calculations in a more structured way before providing the final answer.



\### Advantages



\- Useful for multi-step reasoning.

\- Makes intermediate calculations easier to follow.

\- Can reduce mistakes in problems requiring several reasoning steps.



\### Limitation



CoT does not provide external information by itself. It still depends on the information available to the model.



\---



\## 4. ReAct



ReAct combines reasoning with actions. The agent can decide when a tool is needed, execute the tool, observe its result, and then continue reasoning.



\### Observation



The ReAct implementation used the `course\_info` tool to retrieve course information before producing the final response.



The process follows the general pattern:



\*\*Thought → Action → Observation → Final Answer\*\*



\### Advantages



\- Can use external tools.

\- Useful when information must be retrieved before answering.

\- Combines reasoning and tool usage.



\### Limitation



It requires additional implementation and tool handling compared with direct prompting.



\---



\## 5. Comparison



| Aspect | Direct Prompting | Chain-of-Thought | ReAct |

|---|---|---|---|

| Reasoning depth | Low | Higher | Higher |

| Tool usage | No | No | Yes |

| Multi-step questions | Suitable for simple problems | Useful | Useful |

| Transparency | Direct answer | Shows reasoning steps | Shows reasoning/action process |

| Speed and cost | Generally lower | Higher than direct prompting | Higher because of tool calls |

| Consistency | Usually high at low temperature | Can vary with temperature | Depends on reasoning and tool results |



\---



\## 6. Self-Consistency



Self-consistency was tested by running the Chain-of-Thought reasoning task multiple times with a non-zero temperature.



The answers from the repeated runs were compared to identify the majority answer.



\### Observation



Self-consistency can help identify an answer that appears repeatedly across independent reasoning attempts.



At temperature 0, the model produces a more deterministic response, so repeated runs are expected to be more consistent.



\### Purpose



The experiment demonstrates that multiple reasoning attempts can be compared rather than relying on only one generated reasoning path.



\---



\## 7. Suitability



\### Direct Prompting



Suitable when the question is simple and the required information is already provided.



\### Chain-of-Thought



Suitable when the problem requires several reasoning or calculation steps.



\### ReAct



Suitable when the task requires both reasoning and information obtained through an external tool.



\### Self-Consistency



Suitable when multiple reasoning attempts can be used to check whether an answer is consistent.



\---



\## 8. Conclusion



The experiment demonstrates that the three approaches have different purposes.



Direct prompting is the simplest approach for straightforward questions. Chain-of-Thought provides a structured approach for multi-step reasoning. ReAct extends the process by allowing the model to interact with tools and use their observations.



The suitable approach depends on the requirements of the task: simple questions can use direct prompting, reasoning-heavy questions can use CoT, and tasks requiring external information can use ReAct.

