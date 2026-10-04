# Scope of You — Final Frontier Research Delivery

## Start here
1. `paper/main.pdf` — research paper.
2. `reports/OPENAI_ANTHROPIC_REVIEW_PACKET.md` — compact research-lead review path.
3. `docs/RESEARCH_DECISION_LOG.md` — failed hypotheses and method revisions.
4. `reports/CLAIM_EVIDENCE_MATRIX.md` — claim-to-evidence mapping.
5. `reports/FRONTIER_READINESS_MATRIX.md` — current evidence ceiling and remaining gates.
6. `docs/AGENTIC_EVAL_DESIGN.md` — repeated-trial stateful agent evaluation.
7. `docs/EXTERNAL_EXECUTION_HANDOFF.md` — frozen GPU/human handoff.

## Executed controlled evidence
- PCO-Robust five-seed controlled study.
- Independent ContractBench-Implicit evaluation.
- hierarchical user→case bootstrap.
- ablations and utility/selectivity analysis.
- negative-result retention.
- uncertainty diagnostic and non-inferiority analysis.
- personalization leakage analysis.
- Agentic Contract Suite v2: 288 scenarios × 5 trials, including stale-memory and tool-injection stress.

## External evidence intentionally pending
- two 7–8B generative model families;
- official public-benchmark outcomes at matched scale;
- human labels and blinded response preference;
- production external-tool execution.

These are not represented as completed results. Their experiment matrix, data/result schema, seeds, metrics, human protocol, and execution gates are frozen in the repository.

## Verification
```bash
PYTHONPATH=src pytest -q
make frontier-handoff-check
python scripts/audit_no_project_dates.py
PYTHONPATH=src python scripts/check_release_consistency.py
PYTHONPATH=src python scripts/check_internal_links.py
PYTHONPATH=src python scripts/frontier_research_audit.py --root . --output reports/frontier_research_audit.json
PYTHONPATH=src python -m personal_agi_pt.release_audit --root . --output reports/release_audit.json
```

The public project identifies the author as Aura Yavary. Reviewer-facing anonymous submission artifacts remain separate.
