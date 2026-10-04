import argparse, json
from pathlib import Path

REQUIRED = [
    "docs/OPENAI_ANTHROPIC_RESEARCH_BAR.md",
    "docs/RESEARCH_DECISION_LOG.md",
    "docs/AGENTIC_EVAL_DESIGN.md",
    "reports/OPENAI_ANTHROPIC_REVIEW_PACKET.md",
    "reports/paper_grade_robust_study.json",
    "reports/uncertainty_noninferiority.json",
    "reports/personalization_leakage.json",
    "reports/agentic_contract_suite.json",
    "reports/agentic_contract_suite_v2.json",
    "reports/AGENTIC_EVAL_V2_SUMMARY.md",
    "reports/FRONTIER_READINESS_MATRIX.md",
    "data/agentic_contract_suite.jsonl",
    "data/agentic_contract_suite_v2.jsonl",
    "human_eval/phase_a_items.csv",
    "human_eval/EXECUTION_CHECKLIST.md",
    "configs/llm_paper/matrix.json",
    "configs/frontier/llm_experiment_matrix.json",
    "external_runs/run_plan.json",
    "external_runs/result.schema.json",
    "docs/EXTERNAL_EXECUTION_HANDOFF.md",
]

FORBIDDEN_COMPLETED_CLAIMS = [
    "state-of-the-art on public benchmarks",
    "sota on public benchmarks",
    "human study confirms",
    "production tool-use result",
    "calibrated uncertainty",
]


def audit(root: Path):
    missing = [p for p in REQUIRED if not (root / p).exists()]
    scanned = []
    violations = []
    for rel in ["README.md", "CLAIMS_AND_LIMITATIONS.md", "reports/OPENAI_ANTHROPIC_REVIEW_PACKET.md"]:
        p = root / rel
        if not p.exists():
            continue
        txt = p.read_text(errors="ignore").lower()
        scanned.append(rel)
        for phrase in FORBIDDEN_COMPLETED_CLAIMS:
            idx = txt.find(phrase)
            if idx >= 0:
                prefix = txt[max(0, idx-16):idx]
                if not any(neg in prefix for neg in ["no ", "not ", "without ", "does not claim "]):
                    violations.append({"file": rel, "phrase": phrase})
    agentic = json.loads((root / "reports/agentic_contract_suite.json").read_text()) if (root / "reports/agentic_contract_suite.json").exists() else {}
    agentic_ok = agentic.get("status") == "benchmark sanity-check only; not an LLM performance claim"
    agentic_v2 = json.loads((root / "reports/agentic_contract_suite_v2.json").read_text()) if (root / "reports/agentic_contract_suite_v2.json").exists() else {}
    agentic_v2_ok = agentic_v2.get("status") == "evaluator stress-test only; not an LLM capability result" and agentic_v2.get("n_scenarios") == 288 and agentic_v2.get("trials_per_scenario") == 5
    run_plan = json.loads((root / "external_runs/run_plan.json").read_text()) if (root / "external_runs/run_plan.json").exists() else {}
    handoff_ok = run_plan.get("n_runs") == 36
    result = {
        "passed": not missing and not violations and agentic_ok and agentic_v2_ok and handoff_ok,
        "missing_required_artifacts": missing,
        "unsupported_completed_claims": violations,
        "agentic_result_correctly_scoped": agentic_ok,
        "agentic_v2_correctly_scoped": agentic_v2_ok,
        "external_handoff_matrix_frozen": handoff_ok,
        "claim_files_scanned": scanned,
        "external_gates": [
            "7-8B generative LLM runs",
            "official public-benchmark model outcomes",
            "real human labels",
            "production tool/API execution",
        ],
    }
    return result

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--output", default="reports/frontier_research_audit.json")
    args = ap.parse_args()
    root = Path(args.root)
    result = audit(root)
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
