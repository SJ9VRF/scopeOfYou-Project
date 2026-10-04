from pathlib import Path

from personal_agi_pt.synthetic_dataset import generate_interactions, save_jsonl
from personal_agi_pt.synthetic_users import generate_profiles, save_profiles

ROOT = Path(__file__).resolve().parent
profiles = generate_profiles(100, seed=7)
save_profiles(profiles, ROOT / "synthetic/user_profiles/profiles_v0.2.json")
rows = generate_interactions(profiles, interactions_per_user=12, drift_probability=0.30, seed=11)
save_jsonl(rows, ROOT / "data/samples/synthetic_v0.2.jsonl")
print(f"generated_profiles={len(profiles)}")
print(f"generated_interactions={len(rows)}")
