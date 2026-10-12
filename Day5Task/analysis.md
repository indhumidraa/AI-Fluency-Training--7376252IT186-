# Day 5 - Local Model Alternative Analysis

## Objective
Evaluate an alternative to local LLM execution.

## Tested Configuration
- Provider: Groq
- Model: openai/gpt-oss-20b
- Demo: StudyBuddy

## Benchmark Results
- Non-streaming response time: 0.912 seconds
- Time to first token (TTFT): 0.432 seconds
- Streaming time: 0.665 seconds
- Tokens generated: 250
- Throughput: 375.85 tokens/second

## Functional Test
The StudyBuddy demo generated a response successfully. A prompt override returned three bullet points about linked lists.

## Limitations
Ollama and vLLM hands-on tests were not completed because local model installation was not feasible in the current environment. Groq requires internet access and an API key.

## Conclusion
The Groq API successfully demonstrated LLM inference and streaming without downloading a local model. Local inference remains unverified.
