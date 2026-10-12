# Day 5 Lab - Observations and Discussion

## Environment
- Local Ollama: Not installed
- Inference provider tested: Groq API
- Models tested: openai/gpt-oss-20b and openai/gpt-oss-120b
- vLLM GPU demonstration: Not performed; paper alternative used

## 1. Model benchmark results

| Prompt | Model | Response time | Output tokens | Approx. throughput |
|---|---|---:|---:|---:|
| Reply exactly OK | gpt-oss-20b | 0.8 s | 41 | 50.7 tokens/s |
| Explain an AI agent | gpt-oss-20b | 1.0 s | 213 | 215.1 tokens/s |
| Scholarship calculation | gpt-oss-20b | 1.0 s | 190 | 195.2 tokens/s |
| Reply exactly OK | gpt-oss-120b | 0.8 s | 45 | 54.6 tokens/s |
| Explain an AI agent | gpt-oss-120b | 0.9 s | 103 | 118.6 tokens/s |
| Scholarship calculation | gpt-oss-120b | 1.1 s | 270 | 240.2 tokens/s |

These are measurements from the hosted Groq API, not local Ollama inference.
The load-duration metric is unavailable from this API benchmark.

Expected scholarship calculation:
- Original fee: Rs. 18,000
- Scholarship: 15% of Rs. 18,000 = Rs. 2,700
- Payable amount: Rs. 15,300

## 2. Ollama and Modelfile observations

- Models installed locally: Not tested; Ollama is not installed.
- Model disk size, context length, licence and loaded memory: Not measured.
- fee-assistant and events-announcer: Not built or tested locally.
- Modelfile versus program system prompt precedence: Not tested in Ollama.
- REST endpoints /api/generate, /api/chat, /api/tags and /api/ps: Not tested against Ollama.
- Streaming TTFT: Not measured using the Ollama REST API.

## 3. vLLM paper alternative

### Question 1: KV-cache allocation
With naive contiguous allocation, each request reserves a large continuous memory region based on its maximum expected length. Unused reserved space is wasted, and variable-length requests can cause fragmentation.

With PagedAttention, KV-cache data is stored in fixed-size blocks. With 16-token blocks, each block holds up to 16 tokens. A request can use additional blocks as it grows, reducing external fragmentation and unused reserved capacity. The final block can still have some unused token slots.

### Question 2: Static batching versus continuous batching
In static batching, requests are grouped together and the batch may wait for its longest request to finish before the next batch starts. Short requests can leave GPU capacity idle while longer requests continue.

In continuous batching, completed requests leave the batch and new requests can enter while other requests are still generating. This improves GPU utilization and overall throughput.

### Question 3: Prefix caching
A 900-token system prompt sent in each of six steps is presented six times at the application level. Without prefix caching, its prefix computation may be repeated for each step. With effective prefix caching, the reusable prefix can be computed once and reused for later compatible requests, subject to cache availability and matching prefix conditions.

### Question 4: Throughput and latency
- A larger maximum batch size can improve aggregate throughput by processing more requests together, but may increase the waiting time for an individual request.
- A smaller batch or lower batching delay can reduce individual-request latency, but may reduce aggregate throughput by leaving GPU capacity underused.

Actual effects depend on the workload and server configuration.

## 4. Discussion answers

1. A custom model built from a Modelfile is primarily a configuration layer referencing existing model weights and applying defaults such as a system prompt and parameters; it is not necessarily a separate copy of the base weights.
2. The program can supply task-specific instructions at runtime, allowing an agent framework to adapt behaviour to the current user request and workflow.
3. TTFT matters for interactive chat and streaming user feedback. Total time matters for complete answers, background tasks and multi-step agent workflows.
4. Choose a smaller model when speed and cost dominate and its output passes evaluation. Choose a larger model when its accuracy and instruction-following justify the added latency and cost. Test both on representative tasks.
5. PagedAttention manages KV-cache memory in blocks, while continuous batching dynamically combines active requests. Together, these mechanisms can improve memory use and GPU throughput when serving many students.

## 5. Result

The Groq API alternative was tested with two hosted models on three common prompts. Response time and approximate output-token throughput were recorded. Local Ollama serving, custom Modelfile execution and the vLLM GPU demonstration were not performed. The vLLM section was completed as a theory-based paper alternative.
