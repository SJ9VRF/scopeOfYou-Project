from personal_agi_pt.agentic_eval_v2 import run_suite


def test_agentic_v2_separates_reference_policies():
    r = run_suite(n_trials_per_task=3)
    p = r["policies"]
    assert r["n_scenarios"] == 288
    assert p["contract_oracle"]["trial_success"] == 1.0
    assert p["risk_aware"]["hard_safe"] == 1.0
    assert p["risk_aware"]["trial_success"] > p["naive_personalize"]["trial_success"]
    assert p["naive_personalize"]["by_variant"]["tool_injection"]["hard_safe"] < p["risk_aware"]["by_variant"]["tool_injection"]["hard_safe"]


def test_noisy_policy_exposes_reliability_gap():
    r = run_suite(n_trials_per_task=5)
    noisy = r["policies"]["noisy_risk_aware"]
    assert noisy["pass@5"] > noisy["all_success@5"]
    assert noisy["hard_safe"] < 1.0
