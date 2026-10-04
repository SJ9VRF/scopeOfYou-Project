from __future__ import annotations

import torch

from .schema import InteractionRecord

VERBOSITY_TARGET = {"concise": 0.10, "balanced": 0.50, "detailed": 0.90}


def personalization_target(r: InteractionRecord) -> float:
    """Target for the learned personalization control signal.

    v3 stores an explicit target in metadata. Older datasets fall back to the
    user's verbosity preference so legacy artifacts remain readable.
    """
    explicit = r.metadata.get("personalization_target")
    if explicit is not None:
        return float(explicit)
    verbosity = r.user_state.get("verbosity", "balanced")
    return VERBOSITY_TARGET.get(str(verbosity), 0.50)


def factuality_target(r: InteractionRecord) -> float:
    return 1.0 if r.feedback.factuality is None else float(r.feedback.factuality)


def nonsycophancy_target(r: InteractionRecord) -> float:
    syc = 0.0 if r.feedback.sycophancy is None else float(r.feedback.sycophancy)
    return 1.0 - syc


def proactivity_target(r: InteractionRecord) -> float:
    explicit = r.metadata.get("proactivity_target")
    if explicit is not None:
        return float(explicit)
    return 0.5 if r.feedback.proactivity is None else float(r.feedback.proactivity)


def helpfulness_target(r: InteractionRecord) -> float:
    return 0.5 if r.feedback.helpfulness is None else float(r.feedback.helpfulness)


def behavior_target_dict(r: InteractionRecord) -> dict[str, float]:
    return {
        "personalization": personalization_target(r),
        "factuality": factuality_target(r),
        "sycophancy": 1.0 - nonsycophancy_target(r),
        "proactivity": proactivity_target(r),
        "helpfulness": helpfulness_target(r),
    }


def behavior_target_tensor(r: InteractionRecord) -> torch.Tensor:
    return torch.tensor(
        [
            personalization_target(r),
            factuality_target(r),
            nonsycophancy_target(r),
            proactivity_target(r),
            helpfulness_target(r),
        ],
        dtype=torch.float32,
    )
