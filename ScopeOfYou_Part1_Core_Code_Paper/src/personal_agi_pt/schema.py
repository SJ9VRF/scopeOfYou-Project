from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


ALLOWED_PROVENANCE = {"human", "synthetic", "adversarial", "failure_mined"}
ALLOWED_SPLITS = {"train", "validation", "test"}


@dataclass
class Feedback:
    helpfulness: float | None = None
    personalization: float | None = None
    factuality: float | None = None
    sycophancy: float | None = None
    proactivity: float | None = None
    overall: float | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any] | None) -> "Feedback":
        raw = raw or {}
        return cls(**{k: raw.get(k) for k in cls.__dataclass_fields__})

    def validate(self) -> list[str]:
        errors: list[str] = []
        for name, value in self.__dict__.items():
            if value is not None and not 0.0 <= float(value) <= 1.0:
                errors.append(f"feedback.{name} must be in [0, 1]")
        return errors


@dataclass
class InteractionRecord:
    conversation_id: str
    user_id: str
    user_state: dict[str, Any]
    history: list[dict[str, str]]
    current_query: str
    candidate_response: str
    feedback: Feedback = field(default_factory=Feedback)
    provenance: str = "human"
    confidence: float = 1.0
    dataset_version: str = "v0.1"
    split: str = "train"
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "InteractionRecord":
        payload = dict(raw)
        payload["feedback"] = Feedback.from_dict(payload.get("feedback"))
        return cls(**payload)

    def validate(self) -> list[str]:
        errors: list[str] = []
        for key in ("conversation_id", "user_id", "current_query", "candidate_response"):
            if not getattr(self, key):
                errors.append(f"{key} is required")
        if self.provenance not in ALLOWED_PROVENANCE:
            errors.append(f"provenance must be one of {sorted(ALLOWED_PROVENANCE)}")
        if self.split not in ALLOWED_SPLITS:
            errors.append(f"split must be one of {sorted(ALLOWED_SPLITS)}")
        if not 0.0 <= float(self.confidence) <= 1.0:
            errors.append("confidence must be in [0, 1]")
        if not isinstance(self.user_state, dict):
            errors.append("user_state must be an object")
        if not isinstance(self.history, list):
            errors.append("history must be a list")
        errors.extend(self.feedback.validate())
        return errors
