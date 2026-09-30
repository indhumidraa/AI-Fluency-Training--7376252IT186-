Day 4 - Will It Fit, and May I Use It?
This repository contains the Day 4 conceptual analysis, memory estimator,
and context/quantization experiment.
Scenario
Machine: laptop with 8 GB system RAM
Model-memory budget: 5 GB
Workload: private student study assistant / summariser
Serving: Ollama on CPU
Users: one student
Target: small text model with a practical 4K-8K working context
Date checked: 30 September 2026
Files
`analysis.md` - full written submission
`estimator.py` - memory estimator
`context_quantization.py` - context and quantization sweeps
`screenshots/` - reproducible output plus a place for your actual terminal/model-card screenshots
Run
```bash
python estimator.py
python context_quantization.py
```
For the required estimate-versus-reality section, run the following on the
actual machine:
```bash
ollama pull llama3.2:3b
ollama list
ollama run llama3.2:3b
ollama ps
```
Capture those outputs as screenshots and replace the clearly marked
"local reality" fields in `analysis.md`.
The repository deliberately does not invent `ollama ps` output because
that value must come from a real machine, as required by the Day 4 brief.