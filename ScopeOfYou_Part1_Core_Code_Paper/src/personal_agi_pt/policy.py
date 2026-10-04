from __future__ import annotations

from dataclasses import dataclass

from .schema import InteractionRecord


@dataclass
class PolicyOutput:
    response: str
    behavior: dict[str, float]


class BootstrapPersonalPolicy:
    """A deterministic stand-in for future checkpoints.

    This intentionally does not pretend to be an LLM. It gives the eval stack a
    stable contract before expensive training is introduced.
    """

    def predict(self, record: InteractionRecord) -> PolicyOutput:
        state = record.user_state
        verbosity = state.get("verbosity", "balanced")
        wants_proactivity = float(state.get("proactivity", 0.5))
        query = record.current_query.strip()

        factuality = 1.0
        sycophancy = 0.0
        if "paris is the capital of germany" in query.lower():
            response = "Berlin is the capital of Germany. Paris is the capital of France."
        elif verbosity == "concise":
            response = f"Concise answer: {query[:100]}"
        elif verbosity == "detailed":
            response = f"Detailed answer requested. Key point: {query}"
        else:
            response = f"Answer: {query}"

        return PolicyOutput(
            response=response,
            behavior={
                "personalization": 1.0 if verbosity in {"concise", "detailed"} else 0.5,
                "factuality": factuality,
                "sycophancy": sycophancy,
                "proactivity": min(max(wants_proactivity, 0.0), 1.0),
            },
        )
