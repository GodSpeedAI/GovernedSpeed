from __future__ import annotations

from typing import Any, Dict, List

from policy_gateway.domain.models import (
    CiCheckInput,
    CiCheckResult,
    DecisionResult,
    OutputDecisionInput,
    PromptDecisionInput,
    RulesSnapshot,
)
from policy_gateway.ports.configuration import ConfigurationPort


class PolicyDecisionService:
    """Application service exposing policy decisions over abstract ports."""

    def __init__(self, configuration_port: ConfigurationPort) -> None:
        self._configuration_port = configuration_port

    def health(self) -> Dict[str, str]:
        return {"status": "ok"}

    def rules(self) -> RulesSnapshot:
        config = self._configuration_port.load() or {}
        return RulesSnapshot(raw=config)

    def decide_prompt(self, request: PromptDecisionInput) -> DecisionResult:
        context = request.context or {}
        if context.get("contains_pii") and not context.get("lawful_basis"):
            return DecisionResult(
                allowed=False,
                action="block",
                reasons=["PII without lawful basis"],
            )
        if (context.get("jailbreak_score") or 0) > 0.8:
            return DecisionResult(
                allowed=True,
                action="safe_mode",
                reasons=["high jailbreak score"],
            )
        return DecisionResult(allowed=True, action="allow")

    def decide_output(self, request: OutputDecisionInput) -> DecisionResult:
        context = request.context or {}
        if (context.get("verbatim_ratio") or 0) > 0.2:
            return DecisionResult(
                allowed=True,
                action="summarize",
                reasons=["verbatim over limit"],
            )
        return DecisionResult(allowed=True, action="allow")

    def ci_check(self, request: CiCheckInput) -> CiCheckResult:
        config = self._configuration_port.load() or {}
        thresholds: Dict[str, Any] = config.get("thresholds", {})

        violations: List[str] = []

        quality_target = self._lookup_threshold(thresholds, "quality", "pass_at_5", "target")
        if quality_target is not None and request.quality.get("pass_at_5", 0) < quality_target:
            violations.append("quality.pass_at_5")

        fairness_max = self._lookup_threshold(
            thresholds, "fairness", "subgroup_delta", "target_max"
        )
        if fairness_max is not None and request.fairness.get("subgroup_delta", 0) > fairness_max:
            violations.append("fairness.subgroup_delta")

        safety_max = self._lookup_threshold(thresholds, "safety", "harmful_rate", "target_max")
        if safety_max is not None and request.safety.get("harmful_rate", 0) > safety_max:
            violations.append("safety.harmful_rate")

        status = "fail" if violations else "pass"
        return CiCheckResult(status=status, violations=violations)

    @staticmethod
    def _lookup_threshold(
        thresholds: Dict[str, Any],
        domain_key: str,
        metric_key: str,
        value_key: str,
    ) -> float | None:
        domain_cfg = thresholds.get(domain_key, {})
        metric_cfg = domain_cfg.get(metric_key, {})
        value = metric_cfg.get(value_key)
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
