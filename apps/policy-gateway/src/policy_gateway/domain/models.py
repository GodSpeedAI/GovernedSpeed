from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PromptDecisionInput:
    prompt: str
    context: Dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class OutputDecisionInput:
    output: str
    context: Dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class CiCheckInput:
    quality: Dict[str, float]
    fairness: Dict[str, float]
    safety: Dict[str, float]
    drift: Dict[str, float]


@dataclass(frozen=True)
class DecisionResult:
    allowed: bool
    action: str
    reasons: List[str] = field(default_factory=list)

    def to_response(self) -> Dict[str, object]:
        """Return a plain dict shaped like the HTTP DecisionResponse.

        Keep the return type plain (dict) so the HTTP layer can pass it to
        Pydantic as: DecisionResponse(**decision.to_response()).
        """
        return {
            "allowed": bool(self.allowed),
            "action": self.action,
            "reasons": list(self.reasons or []),
        }


@dataclass(frozen=True)
class CiCheckResult:
    status: str
    violations: List[str] = field(default_factory=list)

    def to_response(self) -> Dict[str, object]:
        """Return a plain dict shaped like the HTTP CiCheckResponse."""
        return {
            "status": self.status,
            "violations": list(self.violations or []),
        }


@dataclass(frozen=True)
class RulesSnapshot:
    raw: Dict[str, object]

    def to_dict(self) -> Dict[str, object]:
        return self.raw


# --- LLM completion models
@dataclass(frozen=True)
class CompletionRequest:
    prompt: str
    # optional model selection and extra parameters
    model: Optional[str] = None
    max_tokens: Optional[int] = None


@dataclass(frozen=True)
class CompletionResponse:
    content: str
    model: Optional[str] = None
    usage: Dict[str, object] = field(default_factory=dict)
