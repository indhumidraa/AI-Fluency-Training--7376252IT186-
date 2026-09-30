#!/usr/bin/env python3
"""
Day 4 Task - Memory estimator for local LLMs.

Formula:
  weights = parameters * bytes_per_parameter
  KV cache = 2 * layers * kv_heads * head_dim * context_tokens * kv_bytes
  total = weights + KV cache + runtime overhead

All decimal GB values are used: 1 GB = 1,000,000,000 bytes.
The runtime-overhead value is deliberately explicit because real runtimes
vary with architecture, backend, build and defaults.
"""

BYTES_PER_PARAMETER = {
    "Q4": 0.5,
    "Q5": 0.625,
    "Q8": 1.0,
    "FP16": 2.0,
    "BF16": 2.0,
}

def gb(n_bytes):
    return n_bytes / 1_000_000_000

def estimate(params_b, precision, context_k, layers, kv_heads,
             head_dim, runtime_overhead_gb=0.5, memory_budget_gb=5.0):
    params = params_b * 1_000_000_000
    weight_bytes = params * BYTES_PER_PARAMETER[precision]

    context_tokens = context_k * 1024
    kv_bytes_per_value = 2  # FP16 KV cache
    kv_bytes = (
        2 * layers * kv_heads * head_dim *
        context_tokens * kv_bytes_per_value
    )

    weights_gb = gb(weight_bytes)
    kv_gb = gb(kv_bytes)
    total_gb = weights_gb + kv_gb + runtime_overhead_gb

    return {
        "weights_gb": weights_gb,
        "kv_gb": kv_gb,
        "total_gb": total_gb,
        "fits": total_gb <= memory_budget_gb,
    }

def print_estimate(name, params_b, precision, context_k, arch,
                   budget_gb=5.0, overhead_gb=0.5):
    r = estimate(
        params_b, precision, context_k,
        arch["layers"], arch["kv_heads"], arch["head_dim"],
        overhead_gb, budget_gb
    )
    print(
        f"{name:30} params={params_b:.2f}B precision={precision:5} "
        f"context={context_k:6}K weights={r['weights_gb']:.3f}GB "
        f"KV={r['kv_gb']:.3f}GB total={r['total_gb']:.3f}GB "
        f"fits={r['fits']}"
    )

if __name__ == "__main__":
    # Llama 3.2 3B: 3.21B params, 28 layers, 8 KV heads, 128 head dimension.
    llama32_3b = {"layers": 28, "kv_heads": 8, "head_dim": 128}

    print("Available model-memory budget: 5.0 GB")
    print("Runtime overhead assumption: 0.5 GB")
    print()

    print("Four configurations:")
    for precision in ("Q4", "Q5", "Q8", "FP16"):
        print_estimate(
            "Llama 3.2 3B", 3.21, precision, 4,
            llama32_3b
        )

    print("\nContext-length sweep, fixed Q4:")
    for context in (2, 8, 32, 128):
        print_estimate(
            "Llama 3.2 3B", 3.21, "Q4", context,
            llama32_3b
        )

    print("\nQuantization sweep, fixed 8K:")
    for precision in ("Q4", "Q5", "Q8", "FP16"):
        print_estimate(
            "Llama 3.2 3B", 3.21, precision, 8,
            llama32_3b
        )
