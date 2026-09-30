# Day 4 Task — Will It Fit, and May I Use It?

**Date checked:** 30 September 2026

## Scenario statement

I am considering a local AI study assistant on a laptop with **8 GB of system RAM**. I reserve **5 GB as the model-memory budget**, leaving the rest for the operating system and other applications. The workload is a private, single-user assistant that can answer questions and summarize study material. I will use a CPU-based Ollama setup because the scenario does not assume a dedicated GPU. I want a small open-weight model and a practical working context of about 4K–8K tokens.

The first decision is therefore not "which model sounds best?" but "will the model fit the available memory, and does its licence permit my intended use?" The Day 4 brief specifically requires the weights, KV cache, runtime overhead, context length, quantization, model card, and licence to be considered together.

---

## 3.1 Explanation of the required concepts

### 1. Model weights

Model weights are the stored numerical parameters of a model. Their memory requirement mainly depends on the number of parameters and the number of bytes used for each parameter.

For the estimator I use:

`weight memory = parameter count × bytes per parameter`

The simplified bytes-per-parameter assumptions are:

| Precision | Approx. bytes/parameter |
|---|---:|
| Q4 | 0.50 |
| Q5 | 0.625 |
| Q8 | 1.00 |
| FP16/BF16 | 2.00 |

For the chosen Llama 3.2 3B model, I use 3.21 billion parameters. At Q4 this gives approximately:

`3.21B × 0.50 bytes = 1.605 GB`

At FP16 the same parameter count would need approximately:

`3.21B × 2.00 bytes = 6.420 GB`

This shows why parameter count alone is not enough: the precision/quantization also changes the stored weight size. Ignoring this could make a model look either much smaller or much larger than the version actually being loaded.

Llama 3.2 3B is available as an instruction-tuned text model, and the official model card describes quantized models as suitable for on-device use cases with limited compute resources. citeturn1search17

### 2. Quantization

Quantization stores model values using fewer bits. In this analysis, moving from FP16 to Q8, Q5 and Q4 reduces the approximate bytes per parameter.

For example, for the 3.21B-parameter Llama model:

- FP16: about 6.420 GB for weights
- Q8: about 3.210 GB
- Q5: about 2.006 GB
- Q4: about 1.605 GB

The saving comes with a quality/accuracy trade-off. Lower-bit quantization can reduce memory and make local serving possible, but the exact effect depends on the model and quantization method. Therefore I treat Q4 as a practical memory-saving choice, not as a claim that Q4 has identical quality to FP16.

The Ollama Llama 3.2 tags page also shows multiple quantized variants, including Q4_K_S, Q4_K_M, Q5 and other builds, with different download sizes. citeturn0search7

If quantization is ignored, I could reject a model unnecessarily because I calculated its FP16 size when the actual local build is quantized. Conversely, assuming an unrealistically small quantized size could make me underestimate memory.

### 3. KV cache and context length

The weights do not grow when the conversation gets longer. The **KV cache does**. It stores attention key/value information for tokens already in the active context.

For this estimate I use:

`KV bytes = 2 × layers × KV heads × head dimension × context tokens × KV bytes/value`

The first `2` represents the K and V tensors. I use FP16 for the KV cache in the simplified estimator, so the value is 2 bytes.

For Llama 3.2 3B I use:

- 28 layers
- 8 KV heads
- 128 head dimension
- 2 bytes per KV value

The 28-layer, 8-KV-head and 128-dimension architecture values are taken from the published Llama 3.2 3B configuration. citeturn3search0

Therefore the KV cache increases approximately linearly with context length.

At 2K tokens, the estimated KV cache is about 0.235 GB. At 8K it is about 0.940 GB. At 32K it is about 3.758 GB, while at 128K it is about 15.032 GB.

This matters especially for an agent that keeps adding tool results to its conversation. A model can fit at a short context and become less comfortable at a long context even though its weights have not changed.

Ollama currently lists Llama 3.2 with a 128K context window, while the model card describes the Llama 3.2 family and its intended assistant/agentic use cases. citeturn0search3turn1search17

### 4. Model card

A model card is the main place to check what the model is, who published it, its intended uses, limitations, supported context, and licensing information.

I used the official model card pages for the three candidate families rather than relying only on a model name. The Llama 3.2 model card states that the model is governed by the Llama 3.2 Community License, while Qwen3-4B is marked Apache-2.0 on its official model repository. Gemma's official model card links to its Terms of Use. citeturn1search17turn1search3turn1search0

Ignoring the model card could lead to choosing a model that fits in memory but has conditions unsuitable for the intended distribution or commercial/public deployment.

### 5. Open-weight vs open-source licensing

"Open-weight" does not automatically mean "open-source under a conventional OSI licence." The weights may be downloadable while use and redistribution remain controlled by a custom licence or terms.

This is important in my scenario because the current workload is private and educational, but a future version might become a public or commercial study assistant.

The three candidates demonstrate this difference:

- **Llama 3.2 3B:** Llama 3.2 Community License, a custom commercial licence agreement. The model card says it is intended for commercial and research use, but use is subject to the licence and Acceptable Use Policy. citeturn1search17
- **Qwen3 4B:** Apache License 2.0. The official model repository identifies the licence as Apache-2.0, and the licence grants broad rights subject to its terms. citeturn1search3turn1search4
- **Gemma 3 4B:** Gemma Terms of Use. Google's current terms govern use, reproduction, modification, distribution and other uses of Gemma. citeturn1search13

Therefore, the exact licence name and its conditions matter more than simply calling all three models "open."

---

# 3.2 Estimate table and model comparison

## (a) Memory estimate table

**Available model-memory budget: 5.0 GB**

The following table is generated by `estimator.py`. Runtime overhead is modeled as 0.5 GB. The estimates use the simplified Day 4 memory approach and are intended for fit decisions, not byte-perfect prediction.

| Model | Params | Precision | Context | Weights (GB) | KV cache (GB) | Total (GB) | Fits in 5 GB? |
|---|---:|---|---:|---:|---:|---:|---|
| Llama 3.2 3B | 3.21B | Q4 | 4K | 1.605 | 0.470 | 2.575 | Yes |
| Llama 3.2 3B | 3.21B | Q5 | 4K | 2.006 | 0.470 | 2.976 | Yes |
| Llama 3.2 3B | 3.21B | Q8 | 4K | 3.210 | 0.470 | 4.180 | Yes |
| Llama 3.2 3B | 3.21B | FP16 | 4K | 6.420 | 0.470 | 7.390 | No |

The important pattern is that changing quantization changes the **weights** substantially, while changing context changes the **KV cache**. The formula is an estimate because real memory also depends on the runtime, architecture, implementation and defaults.

---

## (b) Comparison of three open models

**Card/licence check date: 30 September 2026**

| Basis | Llama 3.2 3B Instruct | Qwen3 4B | Gemma 3 4B |
|---|---|---|---|
| Full model/version | Meta Llama 3.2 3B Instruct | Qwen3 4B | Gemma 3 4B |
| Publisher | Meta | Qwen / Alibaba Cloud | Google DeepMind |
| Total / active parameters | 3.21B | 4.02B | 4.3B |
| MoE? | No | No for 4B dense model | No |
| Context window | 128K | 256K in current Ollama entry | 128K |
| Exact licence | Llama 3.2 Community License Agreement | Apache License 2.0 | Gemma Terms of Use |
| Commercial use | Allowed subject to Llama licence/AUP | Broad use subject to Apache 2.0 terms | Subject to Gemma Terms |
| Extra conditions | Custom licence and Acceptable Use Policy | Apache notices/terms apply | Google Gemma terms and restrictions apply |
| Tool calling stated | Yes / tool use supported in Ollama card | Tools shown by Ollama | Not used as the deciding feature here |
| GGUF / Ollama available | Yes | Yes | Yes |
| Ollama Q4 build size | ~2.0 GB for Q4_K_M | 2.5 GB for Q4_K_M | 3.3 GB for Q4_K_M |
| Estimated total at Q4, 8K | ~3.05 GB | ~3.11 GB* | ~3.80 GB* |
| Fits 5 GB budget? | Yes | Yes | Yes |

\*The Qwen3 and Gemma rows are planning estimates using the same simplified Q4 weight assumption and an explicit architecture/KV-cache assumption; the downloaded Ollama file size is the stronger practical reference for the actual build.

Ollama currently lists Llama 3.2 3B at about 2.0 GB for the default build and 128K context, Qwen3 4B at 2.5 GB and 256K context, and Gemma 3 4B at 3.3 GB and 128K context. citeturn0search3turn1search19turn0search9

The Qwen3 Ollama entry identifies the 4B build as 4.02B parameters, Q4_K_M, and Apache License 2.0. citeturn1search14

Gemma 3's official model card states that the 4B model supports a 128K input context and that Gemma 3 is multimodal. citeturn1search0

---

# 3.3 Context length and quantization observation

I chose **Llama 3.2 3B** for this experiment because its small parameter count makes the relationship between weights, KV cache and quantization easy to see.

## Context length — Q4 fixed

| Setting changed | Value | Weights (GB) | KV cache (GB) | Total (GB) | Fits? |
|---|---:|---:|---:|---:|---|
| Context length | 2K | 1.605 | 0.235 | 2.340 | Yes |
| Context length | 8K | 1.605 | 0.940 | 3.045 | Yes |
| Context length | 32K | 1.605 | 3.758 | 5.863 | No |
| Context length | 128K | 1.605 | 15.032 | 17.137 | No |

The **weights did not change** when the context grew. The KV cache increased because more tokens had to be represented in the attention state. Under this simplified estimate, the full advertised 128K context remains below the 5 GB model-memory budget at Q4. However, I would not automatically run at 128K on an 8 GB laptop because the 5 GB budget is itself a planning limit and the operating system, runtime and actual build also consume memory.

## Quantization — 8K fixed

| Setting changed | Value | Weights (GB) | KV cache (GB) | Total (GB) | Fits? |
|---|---:|---:|---:|---:|---|
| Quantization | Q4 | 1.605 | 0.940 | 3.045 | Yes |
| Quantization | Q5 | 2.006 | 0.940 | 3.446 | Yes |
| Quantization | Q8 | 3.210 | 0.940 | 4.650 | Yes |
| Quantization | FP16 | 6.420 | 0.940 | 7.860 | No |

Here the **KV cache stayed constant** because context length was fixed. The weights changed because precision changed. FP16 crosses the 5 GB model-memory budget even at only 8K context.

For this laptop I would choose **Q4** for the planned study assistant. It leaves the most memory headroom for the runtime and longer contexts. The trade-off is that lower-bit quantization can lose some quality compared with higher precision. If the task became more accuracy-sensitive and memory were increased, Q5 or Q8 would become more reasonable alternatives.

---

# 3.4 Estimate versus reality

The assignment requires at least one model to be actually installed and checked with `ollama list` and `ollama ps`. I have **not fabricated these machine-specific values**.

After installing Ollama and running the model on the actual laptop, use:

```bash
ollama pull llama3.2:3b
ollama list
ollama run llama3.2:3b
ollama ps
```

Record:

| Item | Actual value to record |
|---|---|
| Model | `llama3.2:3b` |
| `ollama list` size | **FILL FROM YOUR TERMINAL** |
| `ollama ps` size | **FILL FROM YOUR TERMINAL** |
| Processor | **FILL: CPU / GPU / split** |
| My estimate | Q4, 8K ≈ 2.222 GB total |
| Difference | **Explain after measuring** |

The estimate should be considered close if its order of magnitude is similar to the observed runtime use. A difference is expected because the simplified formula does not model every allocation made by the Ollama runtime. The actual build's quantization, context default, architecture-specific implementation, memory allocator and runtime overhead can all move the measured value.

The processor field tells me how the model is being executed. A CPU-only result means the model is running from system memory on the processor. A GPU or split result means some or all of the model is being placed on GPU memory. That distinction matters because the practical memory limit and speed are different.

### Screenshot requirement

The final repository should contain screenshots of:

1. `python estimator.py`
2. `python context_quantization.py`
3. `ollama list`
4. `ollama ps`
5. Llama 3.2 model card/licence
6. Qwen3 model card/licence
7. Gemma 3 model card/licence

---

# 3.5 Suitability analysis

For this **private, single-user study assistant on an 8 GB laptop with a 5 GB model-memory budget**, I would use **Llama 3.2 3B Instruct in a Q4 build**, with an initial context around **8K tokens**.

The memory estimate is about 3.045 GB at Q4 and 8K under the simplified estimator, leaving useful headroom inside the 5 GB model-memory budget. The model is also specifically intended for assistant-like and agentic applications such as retrieval and summarization, and Ollama provides a small Q4 build. citeturn1search17turn0search7

The licence is not simply "open source": it is the **Llama 3.2 Community License Agreement**, so I would check the exact terms again before changing the scenario from private study use to a public or commercial product. citeturn1search17

The **runner-up is Qwen3 4B** for this scenario. It is a 4.02B-parameter model, Ollama provides a Q4_K_M build around 2.5 GB, and its official repository identifies Apache License 2.0. It is therefore a strong alternative when the application benefits from Qwen3's capabilities, but its larger parameter count and current Ollama build size give it a larger practical memory footprint than the selected Llama setup. citeturn1search14turn1search3

The recommendation would change if the scenario changed:

- **More memory:** I could move from Q4 toward Q5/Q8 or a larger model.
- **Public/commercial release:** I would make the exact licence and redistribution/hosting conditions a primary gate before choosing.
- **Much longer context:** I would explicitly budget for the increasing KV cache instead of looking only at weight size.
- **Tool-heavy agent:** I would give more importance to documented tool-calling support and reserve extra memory for accumulated context and tool results.
- **Image understanding:** Gemma 3 4B becomes more relevant because its official model card describes multimodal text and image input. citeturn1search0

---

# 3.6 Conclusion

Model size, quantization, context length and licence matter at different stages of model selection.

**Size** is the first practical constraint when memory is limited. For example, on an 8 GB laptop, a large model can be impossible to load even before considering quality.

**Quantization** becomes important when a model is close to the available memory limit. Reducing precision can make a model fit, but it introduces a quality trade-off. In this scenario, Q4 makes the 3.21B model much smaller than FP16.

**Context length** matters when the application keeps long conversations, documents or tool results. The weights stay fixed, but the KV cache grows with the active context. Therefore a model that fits at 4K or 8K tokens should not automatically be assumed to fit comfortably at its maximum context.

**Licence** can become the deciding factor even when memory is sufficient. A model may fit perfectly on the machine but still require careful review of its licence before redistribution, commercial deployment or public hosting. The three candidates illustrate this difference: Llama 3.2 uses a custom Community License, Qwen3 4B uses Apache 2.0, and Gemma uses Google's Gemma Terms of Use. citeturn1search17turn1search3turn1search13

The main lesson is therefore that "small enough to run" and "permitted for my intended use" are separate questions. A responsible local-model choice checks both before downloading and deploying the model.

---

## Sources checked on 30 September 2026

1. Meta Llama 3.2 3B Instruct model card: official Hugging Face model page. citeturn1search17
2. Ollama Llama 3.2 library and tags. citeturn0search3turn0search7
3. Qwen3-4B official model repository. citeturn1search3
4. Ollama Qwen3 4B library entry. citeturn1search14
5. Google Gemma 3 official model card. citeturn1search0
6. Google Gemma Terms of Use. citeturn1search13
7. Day 4 assignment brief supplied for this task. fileciteturn0file0L39-L55

