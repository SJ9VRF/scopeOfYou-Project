from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class SyntheticUserProfile:
    user_id: str
    verbosity: str
    directness: str
    technical_depth: str
    proactivity: float
    confirmation_policy: str
    correction_tolerance: str

    def as_user_state(self) -> dict:
        return asdict(self)


VERBOSITY = ["concise", "balanced", "detailed"]
DIRECTNESS = ["low", "medium", "high"]
TECHNICAL_DEPTH = ["basic", "intermediate", "advanced"]
CONFIRMATION = ["always", "irreversible_only", "minimal"]
CORRECTION = ["gentle", "neutral", "direct"]


def generate_profiles(n: int, seed: int = 7) -> list[SyntheticUserProfile]:
    rng = random.Random(seed)
    profiles = []
    for i in range(n):
        profiles.append(
            SyntheticUserProfile(
                user_id=f"syn-{i:04d}",
                verbosity=rng.choice(VERBOSITY),
                directness=rng.choice(DIRECTNESS),
                technical_depth=rng.choice(TECHNICAL_DEPTH),
                proactivity=round(rng.uniform(0.0, 1.0), 2),
                confirmation_policy=rng.choice(CONFIRMATION),
                correction_tolerance=rng.choice(CORRECTION),
            )
        )
    return profiles


def save_profiles(profiles: list[SyntheticUserProfile], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(p) for p in profiles], indent=2), encoding="utf-8")
