# Controlled Insurance Claims Benchmark (Phase 2 scaffolding)

Stub scaffold for a 10-agent EU private health insurance claims-adjudication benchmark:

- **Pipeline**: intake → coverage → medical → fraud → decision → (payment + provider) → compliance → legal → analytics
- **Unit of simulation**: single policyholder per trial
- **Failure profiles**: 8 data-level profiles (P1–P8)
- **Scoring**: deterministic 7-check rubric (0–7), no LLM-as-judge
- **Arms**: `v3_off`, `v3_warn`, `v3_intervene`

All modules are stubs for now; entry points raise `NotImplementedError`.

