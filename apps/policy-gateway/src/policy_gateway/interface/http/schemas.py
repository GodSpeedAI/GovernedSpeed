from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, Field


class PromptCheckRequest(BaseModel):
    prompt: str
    context: Dict[str, Any] | None = None


class OutputCheckRequest(BaseModel):
    output: str
    context: Dict[str, Any] | None = None


class CiCheckRequest(BaseModel):
    quality: Dict[str, float]
    fairness: Dict[str, float]
    safety: Dict[str, float]
    drift: Dict[str, float]


class DecisionResponse(BaseModel):
    allowed: bool
    action: str
    reasons: list[str] = Field(default_factory=list)


class CiCheckResponse(BaseModel):
    status: str
    violations: list[str] = Field(default_factory=list)


class CompletionRequest(BaseModel):
    prompt: str
    model: str | None = None
    max_tokens: int | None = None


class CompletionResponse(BaseModel):
    content: str
    model: str | None = None
    usage: Dict[str, object] | None = None
