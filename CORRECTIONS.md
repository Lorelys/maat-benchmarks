# Corrections — September 2026

This file records a correction to the results published in this repository in July 2026 and in version 1 of the arXiv article *Maat: Deterministic Contract-Based Governance for Multi-Agent LLM Workflows*. The original result files are kept unchanged below this notice so the history stays auditable. Corrected figures are summarised here and in the updated `README.md`.

## What was wrong

**1. Halt attribution in the scorers.** The benchmark documentation states that a protective halt counts as a prevented defect only when the finding that caused it corresponds to the injected defect. The deterministic scorers did not do this in three of six benchmarks:

- **B2B financial, hospital triage, software development:** any halt before the final artefact received full marks (7/7), whatever caused it.
- **E-commerce and insurance:** any blocking finding counted as attribution.

As a result, halts on *correct* agent output were counted as successes.

**2. Insurance payout answer key.** The expected payout was not conditioned on the scenario. For the excluded-treatment and fraud profiles, agents that correctly denied the claim (€0) were marked wrong in the ungoverned arm.

**3. Validator defects causing false alarms.** A hand review of all 94 halts in the governed (intervene) arms found:

| | Halts |
|---|---|
| Stopped the injected defect | 45 |
| Stopped a genuine defect that was not injected (e.g. deal total ≠ sum of line items, missing required field, out-of-network payout) | 13 |
| Legitimate escalation (agent could not determine a payout) | 1 |
| **False alarm on correct output** | **35 (37%)** |

False alarms by benchmark:

| Benchmark | False alarms / halts |
|---|---|
| Hospital | 17 / 22 |
| B2B | 8 / 20 |
| Insurance | 6 / 22 |
| Software dev | 3 / 7 |
| E-commerce | 1 / 18 |
| Enterprise | 0 / 5 |

Causes:
- **(22 halts) Provenance check at maximum depth.** Circuit-breaker state carried over between trials raised validation to its strictest depth, where provenance was mandatory. The provenance check recognised only a top-level `provenance` key and ignored field-level and per-item provenance the agents had supplied.
- **(8) Legitimate "none" answers treated as empty.** Examples: a patient with no declared allergies, no documented history.
- **(4) Correct €0 insurance denials.** These were compared with a payable-claim expected amount.
- **(1) Tax parsing.** Per-country transaction counts were parsed as VAT rates.

**4. Statements in this repository that were not supported.** Each item below is followed by what the audit found.

- *"Maat improved output correctness on every benchmark."* Does not survive attribution-aware scoring (see below).
- *"Zero false positives"* (insurance, `WORKSTREAM_B_CONSOLIDATED.md`) and *"False positives in Maat arms: none"* (`CAUGHT_SCENARIOS.md` §1). Both are incorrect.
- *Insurance P3 excluded treatment, "not manifested — self-corrected".* In one warn-arm trial the defect did manifest: €6,930 was approved for an excluded treatment on the strength of a fabricated prior authorization. Maat did not flag it.
- *B2B usage inflation and hospital patient-ID drift listed as caught.* Neither was caught by the intended mechanism in the governed grid runs.
- *Hospital "halt rate up to 100%" per profile.* This was a halt rate, not a catch rate. For example, all 5 disposition-contradiction halts were false alarms at intake.
- *E-commerce un-injected revenue mis-report "detected in 100% of cases".* It was recorded as a **warning** and did not stop the chain.

## Corrected results

Correctness is the mean of the 0–7 rubric. There are three views:
- **v1**: as originally published.
- **Paired**: only (profile, seed) pairs where the governed run completed or halted on an attributable finding; *n* = pairs kept out of governed trials.
- **Lower bound**: every unattributed halt scored as delivering no correct output.

Insurance uses the scenario-conditioned payout key.

| Benchmark | v1 Δ | Paired Δ | n | Lower bound Δ | Halts (unattributed) | Cost Δ v1 | Cost Δ paired |
|---|---|---|---|---|---|---|---|
| B2B financial | +26.5% | +29.1% | 17/25 | −15.9% | 20 (8) | −50% | −47% |
| Hospital triage | +12.4% | +11.1% | 9/25 | −60.8% | 22 (16) | −49% | −21% |
| Software development | +3.8% | +0.8% | 19/25 | −23.1% | 7 (6) | −8% | −1% |
| Enterprise discovery | +7.7% | +7.7% | 30/30 | +7.7% | 5 (0) | ~0% | ~0% |
| E-commerce agency | +10.7% | +10.6% | 44/45 | +8.3% | 18 (1) | −17% | −17% |
| Health insurance | +2.9% | +19.1%* | 16/24 | −21.1% | 22 (8) | −55% | −53% |

\* The paired insurance subset excludes both deny profiles. On the full insurance grid with the corrected key, the result is 5.92 (off) vs 5.83 (intervene), i.e. **−1.4%**.

**How to read this:**
- Where Maat halts on a verifiable defect, it prevents that defect from propagating. This holds clearly for tax/VAT, data residency, identity drift, coverage limits, price drift, discount limits and scope.
- The claim that Maat improves correctness on every workflow is withdrawn. In four of six workflows, the governed arm scored below the ungoverned arm once false-alarm halts are counted as failed work.
- Much of the reported cost saving in B2B and hospital came from stopping correct work.

The B2B paired estimate includes 8 halts on a genuine but un-injected arithmetic error in the deal record. The B2B anchor encodes a single customer's contract for all five customer seeds, so anchor-based B2B checks are meaningful for one seed only.

## What has been fixed since

**Validator fixes:**
- Provenance is recognised anywhere in the payload, and required only where the contract (or a plan-level "always require provenance" policy) asks for it.
- Circuit-breaker state is scoped per workflow, so one run's history no longer changes another run's verdict.
- Legitimate empty answers are accepted when confirmed by the anchor or allowed by the contract.
- Undeclared list fields are no longer treated as contradictory.
- Insurance denials are judged against the upstream exclusion or fraud findings.
- Exclusion evidence at coverage and unverifiable authorizations now block. This closes the €6,930 case.
- Self-declared anchor claims are verified. Dose ranges, "NKDA" and tax parsing are handled.

**Scorer fixes:** a halt earns credit only when the benchmark confirms the injected defect and a specific (non-generic) finding caused the halt.

**Offline validation:** all 573 saved trial outputs were replayed through the old and new validator. Results:
- 33 of the 35 false alarms no longer occur.
- The remaining 2 now halt earlier, on a genuine coverage error.
- All 58 genuine catches are retained.

A live re-run with fresh model calls has not yet been performed. These results will be published here when it is.

## What has not changed

- No language model is used in the validation or scoring path.
- Maat's deterministic behaviour: the same input and configuration produce the same verdict.
- The benchmark designs, defect profiles and raw aggregate files in `results/`. They are left as published and are superseded by the table above.
