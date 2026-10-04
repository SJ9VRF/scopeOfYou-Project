from personal_agi_pt.agentic_eval import generate_suite, run_suite, run_trial

def test_agentic_suite_has_stateful_tasks_and_expected_size():
    tasks = generate_suite()
    assert len(tasks) == 96
    assert len({t.task_id for t in tasks}) == 96
    assert {t.domain for t in tasks} == {"email", "calendar", "files", "settings", "travel", "purchase"}

def test_oracle_satisfies_contract_and_protected_state():
    for task in generate_suite():
        r = run_trial(task, "contract_oracle")
        assert r["graders"]["action_contract"] == 1.0
        assert r["graders"]["protected_boundary"] == 1.0

def test_benchmark_discriminates_naive_from_risk_aware():
    r = run_suite()
    assert r["policies"]["contract_oracle"]["score"] == 1.0
    assert r["policies"]["risk_aware"]["score"] > r["policies"]["naive_personalize"]["score"]
    assert r["policies"]["risk_aware"]["protected_boundary"] >= r["policies"]["naive_personalize"]["protected_boundary"]
