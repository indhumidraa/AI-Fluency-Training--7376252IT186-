# Day 6 Task – Reliable Tool Calling

## 1. Chat Completions

Chat Completions is an API interface where an application sends a list of messages to a model and receives a model-generated response.

A typical request contains:
- system instructions
- user messages
- optional tools
- model parameters such as `max_tokens`

For tool calling, the model can return structured tool-call information instead of only normal text.

---

## 2. OpenAI-Compatible Servers

An OpenAI-compatible server provides an API that follows the request and response format used by the OpenAI API.

This allows the same Python SDK style to work with different providers by changing the API key, base URL, and model.

In this project, Groq is accessed using the OpenAI Python client with a Groq OpenAI-compatible base URL.

---

## 3. Streaming

Streaming sends the model response in smaller pieces as it is generated instead of waiting for the complete response.

Advantages:
- lower perceived waiting time
- useful for chat applications
- allows partial output to be displayed

For reliable tool calling, the application must correctly handle streamed tool-call information if streaming is enabled.

---

## 4. Responses API

The Responses API is a newer API interface designed for more general model interactions and agentic workflows.

It can support text generation, structured outputs, and tool-based workflows in a unified interface.

Chat Completions is still useful for learning and for providers that expose OpenAI-compatible Chat Completions endpoints.

---

# 5. Five-Step Tool-Calling Flow

A reliable tool-calling workflow can be implemented as five steps:

### Step 1 – Model decides

The user sends a request and the model decides whether one or more available tools are needed.

### Step 2 – Parse the tool call

The application reads:
- tool name
- tool-call ID
- JSON argument string

### Step 3 – Look up and validate

The application checks whether the requested tool exists and validates its arguments against the shared schema.

### Step 4 – Execute safely

Only validated arguments are passed to the actual Python function.

Any execution error is converted into a string rather than crashing the entire agent.

### Step 5 – Return the result

The application sends one tool message for every tool call ID.

The model then receives the tool results and can produce the final answer or request another corrected tool call.

---

# 6. Tool Schemas

This project uses a shared `SCHEMAS` dictionary in `tools.py`.

Each schema contains important fields.

### `description`

Explains what the tool does and helps the model understand when the tool should be used.

### `properties`

Defines the accepted arguments and their types.

Example:

```json
{
  "days": {
    "type": "integer"
  }
}