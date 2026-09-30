#!/usr/bin/env python3
"""Generate the Day 4 context/quantization observation table."""
from estimator import estimate

ARCH = {"layers": 28, "kv_heads": 8, "head_dim": 128}
BUDGET = 5.0
OVERHEAD = 0.5

def row(label, precision, context_k):
    r = estimate(3.21, precision, context_k, **ARCH,
                 runtime_overhead_gb=OVERHEAD, memory_budget_gb=BUDGET)
    print(f"{label:25} weights={r['weights_gb']:.3f}GB "
          f"KV={r['kv_gb']:.3f}GB total={r['total_gb']:.3f}GB "
          f"fits={r['fits']}")

print("Context length, same Q4:")
for k in (2, 8, 32, 128):
    row(f"Context {k}K", "Q4", k)

print("\nQuantization, same 8K context:")
for q in ("Q4", "Q5", "Q8", "FP16"):
    row(f"Quantization {q}", q, 8)
