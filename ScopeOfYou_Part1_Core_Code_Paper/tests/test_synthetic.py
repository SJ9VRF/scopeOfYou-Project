from personal_agi_pt.synthetic_dataset import generate_interactions
from personal_agi_pt.synthetic_users import generate_profiles


def test_profile_generation_is_deterministic():
    assert generate_profiles(3, seed=1) == generate_profiles(3, seed=1)


def test_interactions_include_drift_metadata():
    profiles = generate_profiles(4, seed=1)
    rows = generate_interactions(profiles, interactions_per_user=6, drift_probability=1.0, seed=1)
    assert len(rows) == 24
    assert any(r["metadata"]["preference_drift"] for r in rows)
