PYTHONPATH=src
.PHONY: novelty contract test reproduce reproduce-v2 ablations bootstrap doctor export-llm smoke artifacts paper install-offline service-smoke benchmark-smoke audit consistency links project-page-audit release-check

novelty:
	PYTHONPATH=$(PYTHONPATH) python scripts/run_boundary_novelty_lab.py

contract:
	PYTHONPATH=$(PYTHONPATH) python scripts/run_contract_lab.py

test:
	PYTHONPATH=$(PYTHONPATH) pytest -q

bootstrap:
	PYTHONPATH=$(PYTHONPATH) python -m personal_agi_pt.pipeline --dataset data/samples/seed.jsonl --report reports/bootstrap_report.json

# Primary reproducible paper run.
reproduce:
	PYTHONPATH=$(PYTHONPATH) python scripts/run_v31_paper_lab.py

# Superseded clean-v2 run retained for audit history.
reproduce-v2:
	PYTHONPATH=$(PYTHONPATH) python scripts/run_v2_clean_lab.py

ablations:
	PYTHONPATH=$(PYTHONPATH) python scripts/run_v31_ablations_resume.py

doctor:
	PYTHONPATH=$(PYTHONPATH) python -m personal_agi_pt.cli doctor

export-llm:
	PYTHONPATH=$(PYTHONPATH) python -m personal_agi_pt.cli export-sft-splits --source data/samples/personalbench_v31.jsonl --output-dir data/exports
	PYTHONPATH=$(PYTHONPATH) python -m personal_agi_pt.cli export-dpo --source data/samples/preferences_v31.jsonl --output data/exports/dpo_pairs.jsonl

service-smoke:
	PYTHONPATH=$(PYTHONPATH) python scripts/service_smoke.py

benchmark-smoke:
	PYTHONPATH=$(PYTHONPATH) python -m personal_agi_pt.benchmark_runner --dataset data/samples/personalbench_v31.jsonl --checkpoint checkpoints/post_trained_v31_raw.pt --reference-checkpoint checkpoints/sft_behavior_v31.pt --split test --draws 200 --output reports/benchmark_smoke.json >/dev/null

# Audit text artifacts for obvious committed secrets and generate file hashes/provenance.
audit:
	PYTHONPATH=$(PYTHONPATH) python -m personal_agi_pt.release_audit --root . --output reports/release_audit.json

consistency:
	PYTHONPATH=$(PYTHONPATH) python scripts/check_release_consistency.py

links:
	PYTHONPATH=$(PYTHONPATH) python scripts/check_internal_links.py

project-page-audit:
	PYTHONPATH=$(PYTHONPATH) python scripts/check_project_page.py

smoke: test doctor export-llm service-smoke benchmark-smoke consistency links

artifacts:
	PYTHONPATH=$(PYTHONPATH) python scripts/generate_paper_artifacts.py

paper: artifacts
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null && pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
	rm -f paper/main.aux paper/main.log paper/main.out

install-offline:
	python -m pip install -e . --no-build-isolation

release-check: test contract doctor export-llm service-smoke benchmark-smoke public-benchmark-smoke consistency links project-page-audit artifacts paper audit date-audit
	PYTHONPATH=$(PYTHONPATH) python scripts/generate_sbom.py
	@echo "Release checks passed. Primary benchmarks: PersonalBench v3.1 + PersonalBench-Contract"

public-benchmark-smoke:
	PYTHONPATH=$(PYTHONPATH) python -m personal_agi_pt.public_benchmarks normalize --benchmark benchpres --input tests/fixtures/public_benchmarks/benchpres.jsonl --output reports/benchpres_normalized_smoke.jsonl
	PYTHONPATH=$(PYTHONPATH) python -m personal_agi_pt.public_benchmarks score-selectivity --gold reports/benchpres_normalized_smoke.jsonl --predictions tests/fixtures/public_benchmarks/benchpres_predictions.jsonl --output reports/benchpres_selectivity_smoke.json

.PHONY: date-audit
date-audit:
	python scripts/audit_no_project_dates.py

.PHONY: paper-readiness-check
paper-readiness-check: test date-audit consistency links rigor-analysis
	python scripts/validate_llm_paper_matrix.py
	PYTHONPATH=$(PYTHONPATH) python scripts/prepare_human_eval.py --n 500 >/dev/null
	@test -f reports/paper_grade_robust_study.json
	@test -f reports/consistency_regularization_negative.json
	@test -f data/contractbench_implicit.jsonl
	@test -f PAPER_READINESS_AUDIT.md
	@echo "Paper readiness checks passed for executed controlled evidence. LLM/human outcomes remain external execution gates."

.PHONY: rigor-analysis
rigor-analysis:
	PYTHONPATH=$(PYTHONPATH) python scripts/analyze_uncertainty_and_noninferiority.py
	PYTHONPATH=$(PYTHONPATH) python scripts/analyze_personalization_leakage.py

.PHONY: anonymity-audit
anonymity-audit:
	PYTHONPATH=$(PYTHONPATH) python scripts/audit_anonymity.py .

.PHONY: agentic-eval frontier-audit
agentic-eval:
	PYTHONPATH=$(PYTHONPATH) python scripts/run_agentic_contract_suite.py --output reports/agentic_contract_suite.json

frontier-audit: test rigor-analysis agentic-eval date-audit consistency links
	@test -f docs/OPENAI_ANTHROPIC_RESEARCH_BAR.md
	@test -f docs/RESEARCH_DECISION_LOG.md
	@test -f docs/AGENTIC_EVAL_DESIGN.md
	@test -f reports/OPENAI_ANTHROPIC_REVIEW_PACKET.md
	@test -f reports/agentic_contract_suite.json
	PYTHONPATH=$(PYTHONPATH) python scripts/frontier_research_audit.py --root . --output reports/frontier_research_audit.json
	@echo "Frontier research audit passed. External LLM/human gates remain explicitly pending."

.PHONY: agentic-eval-v2 frontier-plan frontier-handoff-check frontier-audit-v2
agentic-eval-v2:
	PYTHONPATH=$(PYTHONPATH) python scripts/run_agentic_contract_suite_v2.py
	python scripts/render_agentic_v2_demo.py

frontier-plan:
	PYTHONPATH=$(PYTHONPATH) python scripts/plan_frontier_runs.py

frontier-handoff-check: frontier-plan
	@test -f external_runs/result.schema.json
	@test -f docs/EXTERNAL_EXECUTION_HANDOFF.md
	@test -f human_eval/EXECUTION_CHECKLIST.md
	@python -c "import json,pathlib; p=json.loads(pathlib.Path('external_runs/run_plan.json').read_text()); assert p['n_runs']==36; print('Frontier handoff check: PASS (36 frozen external LLM runs)')"

frontier-audit-v2: test rigor-analysis agentic-eval-v2 frontier-handoff-check date-audit consistency links
	@test -f reports/AGENTIC_EVAL_V2_SUMMARY.md
	@test -f reports/FRONTIER_READINESS_MATRIX.md
	@test -f reports/agentic_contract_suite_v2.json
	PYTHONPATH=$(PYTHONPATH) python scripts/frontier_research_audit.py --root . --output reports/frontier_research_audit.json
	@echo "Frontier audit v2 passed. External LLM/human outcomes remain pending by construction."


.PHONY: verify-reviewer
verify-reviewer:
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_experiment_ledger.py
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_citation_provenance.py
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_reviewer_bundle.py

.PHONY: verify-frontier
verify-frontier:
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_research_ownership.py
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_experiment_ledger.py
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_citation_provenance.py
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_frontier_artifact.py
	PYTHONPATH=$(PYTHONPATH) pytest -q
	PYTHONPATH=$(PYTHONPATH) python scripts/check_release_consistency.py
	PYTHONPATH=$(PYTHONPATH) python scripts/check_internal_links.py
	PYTHONPATH=$(PYTHONPATH) python scripts/frontier_research_audit.py --root . --output reports/frontier_research_audit.json
	@echo "Frontier artifact verified: executed evidence consistent; external LLM/human gates remain pending."

.PHONY: provenance
provenance:
	PYTHONPATH=$(PYTHONPATH) python scripts/build_experiment_ledger.py
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_experiment_ledger.py

.PHONY: verify-evidence
verify-evidence:
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_research_ownership.py
	PYTHONPATH=$(PYTHONPATH) pytest -q tests/test_evidence_layer.py
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_experiment_ledger.py
	PYTHONPATH=$(PYTHONPATH) python scripts/check_project_page.py
	@echo "Evidence layer verified: journal, failures, decisions, raw artifacts, project-page links, and provenance are consistent."

.PHONY: verify-ownership
verify-ownership:
	PYTHONPATH=$(PYTHONPATH) python scripts/build_red_team_coverage.py
	PYTHONPATH=$(PYTHONPATH) python scripts/verify_research_ownership.py
	@echo "Research ownership, failure taxonomy, threat model, and red-team coverage verified."
