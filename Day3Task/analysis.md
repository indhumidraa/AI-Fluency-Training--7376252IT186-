# Day 3 Task - From Prompt to Action

## Scenario: Shopping Bill Calculator

### 1. Introduction

For this task, I chose a simple shopping bill scenario. The purpose is to compare a plain Large Language Model (LLM) with the same LLM when it has access to one external calculation tool.

The tool used in this project is called `calculate_bill`. It calculates the total cost of shopping items using their price and quantity.

For example, if a customer buys 3 notebooks at Rs. 80 each and 2 pens at Rs. 20 each, the tool calculates the total as Rs. 280.

This scenario shows that some questions can be answered directly by an LLM, while numerical questions can be handled more reliably when the model has access to an appropriate tool.

---

## 2. Explanation of Concepts

### What is a Large Language Model?

A Large Language Model is an AI model trained on a large amount of text. It can understand natural language and generate responses based on patterns learned during training.

In this shopping scenario, a plain LLM can answer questions such as "What is a shopping bill?" or "Why is it useful to keep a shopping bill?" without needing an external tool.

However, when asked to perform a numerical calculation, the model is generating the answer rather than actually using a dedicated calculator. This means there can be a risk of arithmetic mistakes.

For example, the question:

"I bought 3 notebooks at Rs. 80 each and 2 pens at Rs. 20 each. What is the total bill?"

requires the calculation:

3 × 80 + 2 × 20 = 280.

A dedicated calculation tool can perform this operation directly.

---

### What is an Agent?

An agent is an LLM-based system that can decide when it needs to use external tools to complete a task.

A plain chat response simply receives a question and generates an answer.

In this project, the tool-enabled system can receive a shopping question, determine that a calculation is required, call the `calculate_bill` tool, receive the result, and then use that result to produce the final response.

Therefore, the important difference is that the tool-enabled system can take an action outside the LLM's normal text generation process.

---

### What is a Tool and a Tool Call?

A tool is an external function that an LLM can use to perform a specific operation.

In this project, the tool is:

`calculate_bill`

Its purpose is to calculate the total shopping cost.

A tool call is the request made by the model to use that function.

The tool schema tells the model:

- the name of the tool
- what the tool does
- what parameters it accepts
- what information must be provided

The model needs this description because it must know what the tool is capable of before deciding whether the tool is appropriate for a question.

For example, the tool expects shopping items containing a name, price and quantity.

---

## 3. Step-by-Step Tool Call Flow

The tool call in this project works as follows.

### Step 1 - User asks a question

The user asks:

"I bought 3 notebooks at Rs. 80 each and 2 pens at Rs. 20 each. What is the total bill?"

### Step 2 - Model receives the question

The LLM receives the question along with the description of the available `calculate_bill` tool.

### Step 3 - Model decides that the tool is useful

The question requires a numerical calculation, so the model can decide to call the calculation tool.

### Step 4 - Model creates the tool call

The model provides the required information to the tool, including the item names, prices and quantities.

### Step 5 - Tool runs

The Python function calculates:

3 × 80 + 2 × 20 = 280

The tool returns:

"Total shopping bill: Rs. 280"

### Step 6 - Result goes back to the model

The tool result is added to the conversation so the LLM can see the calculated value.

### Step 7 - Model gives the final answer

The LLM uses the tool result and responds that the total shopping bill is Rs. 280.

This demonstrates the complete flow from user question to tool call and finally to the answer.

---

## 4. Why Should a Tool Return Text Instead of Stopping the Program?

A tool should return its result as text because the LLM can then receive and interpret the result as part of the conversation.

If the tool encounters a problem, returning an error message as text allows the program to continue and gives the model information about what went wrong.

For example, instead of immediately stopping the entire program, a tool could return:

"Unable to calculate the bill because the quantity is missing."

The model can then explain the problem to the user.

This makes the interaction more robust.

---

## 5. Comparison Table

| Basis for comparison | Plain LLM prompt (no tool) | LLM with one tool |
|---|---|---|
| Source of the answer | Generated from the model's learned knowledge | Can use the model's knowledge plus the tool result |
| Can it fetch or compute information outside its own memory? | No external tool is available | Yes, it can use the provided calculation tool |
| Reliability on factual or numeric questions | Can make arithmetic mistakes | The calculation is performed by the tool |
| Transparency | The calculation process is not performed by an external function | The tool call and its result can be observed |
| Speed / cost | Usually simpler and requires only one model response | Requires a tool call and may require another model response |

---

## 6. Observation

I tested three questions using both versions.

### Question 1

"What is a shopping bill?"

The plain LLM could answer this question without a tool because it is a general conceptual question.

The tool-enabled LLM also answered the question without needing to call the calculation tool.

This shows that a tool is not necessary for every question.

### Question 2

"I bought 3 notebooks at Rs. 80 each and 2 pens at Rs. 20 each. What is the total bill?"

This question requires arithmetic.

The plain LLM generated an answer directly.

The tool-enabled version recognised that the calculation tool could be used. It called `calculate_bill`, passed the item information, received the result Rs. 280, and used that result in its final answer.

This demonstrates the main benefit of giving an LLM access to a tool.

### Question 3

"Why is it useful to keep a shopping bill?"

The plain LLM could answer this question from its general knowledge.

The tool-enabled LLM also answered without needing the calculation tool.

Therefore, the tool was useful for the numerical question but unnecessary for the general conceptual questions.

---

## 7. Suitability and Conclusion

The plain LLM prompt was sufficient for general questions about shopping bills, such as what a shopping bill is and why it is useful.

However, when the question required a numerical calculation, providing an external calculation tool made the process more reliable because the calculation was performed by the tool rather than being generated only as text by the model.

This small experiment shows the difference between an LLM and an agent-like system with tool access.

A plain LLM is suitable when the required answer can reasonably be generated from its learned knowledge.

A tool becomes useful when the task requires an operation, calculation, lookup, or information that the model should not be expected to obtain reliably from its internal knowledge alone.

Therefore, even a single external tool can make an LLM system more useful for tasks that require actions or operations outside ordinary text generation.