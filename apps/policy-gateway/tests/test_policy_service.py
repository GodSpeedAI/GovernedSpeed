from __future__ import annotations

import json
from pathlib import Path

import yaml
from policy_gateway.application.services import PolicyDecisionService
from policy_gateway.domain.models import (
    CiCheckInput,
    OutputDecisionInput,
    PromptDecisionInput,
)
from policy_gateway.infrastructure.config_file_adapter import ConfigFileAdapter
from policy_gateway.ports.configuration import ConfigurationPort


class InMemoryConfigAdapter(ConfigurationPort):
    def __init__(self, data: dict):
        self._data = data

    def load(self) -> dict:
        return self._data


def create_service(config: dict | None = None) -> PolicyDecisionService:
    return PolicyDecisionService(InMemoryConfigAdapter(config or {}))


def test_prompt_blocks_when_pii_without_basis():
    service = create_service()
    request = PromptDecisionInput(prompt="hi", context={"contains_pii": True})
    result = service.decide_prompt(request)
    assert result.allowed is False
    assert result.action == "block"
    assert "PII without lawful basis" in result.reasons


def test_prompt_allows_when_pii_with_lawful_basis():
    service = create_service()
    request = PromptDecisionInput(
        prompt="hi", context={"contains_pii": True, "lawful_basis": "consent"}
    )
    result = service.decide_prompt(request)
    assert result.allowed is True
    assert result.action != "block"
    assert "PII without lawful basis" not in result.reasons


def test_prompt_safe_mode_when_jailbreak_high():
    service = create_service()
    request = PromptDecisionInput(prompt="hi", context={"jailbreak_score": 0.9})
    result = service.decide_prompt(request)
    assert result.allowed is True
    assert result.action == "safe_mode"


def test_output_summarize_when_verbatim_high():
    service = create_service()
    request = OutputDecisionInput(output="o", context={"verbatim_ratio": 0.3})
    result = service.decide_output(request)
    assert result.allowed is True
    assert result.action == "summarize"


def test_output_no_summarize_when_verbatim_at_threshold():
    service = create_service()
    request = OutputDecisionInput(output="o", context={"verbatim_ratio": 0.2})
    result = service.decide_output(request)
    assert result.allowed is True
    assert result.action != "summarize"


def test_output_no_summarize_when_verbatim_below_threshold():
    service = create_service()
    request = OutputDecisionInput(output="o", context={"verbatim_ratio": 0.19})
    result = service.decide_output(request)
    assert result.allowed is True
    assert result.action != "summarize"


def test_ci_check_detects_violations():
    cfg = {
        "thresholds": {
            "quality": {"pass_at_5": {"target": 0.8}},
            "fairness": {"subgroup_delta": {"target_max": 0.2}},
            "safety": {"harmful_rate": {"target_max": 0.1}},
        }
    }
    service = create_service(cfg)
    request = CiCheckInput(
        quality={"pass_at_5": 0.7},
        fairness={"subgroup_delta": 0.3},
        safety={"harmful_rate": 0.2},
        drift={},
    )
    result = service.ci_check(request)
    assert result.status == "fail"
    assert set(result.violations) == {
        "quality.pass_at_5",
        "fairness.subgroup_delta",
        "safety.harmful_rate",
    }


def test_ci_check_passes_when_within_thresholds():
    cfg = {
        "thresholds": {
            "quality": {"pass_at_5": {"target": 0.6}},
            "fairness": {"subgroup_delta": {"target_max": 0.3}},
            "safety": {"harmful_rate": {"target_max": 0.2}},
        }
    }
    service = create_service(cfg)
    request = CiCheckInput(
        quality={"pass_at_5": 0.7},
        fairness={"subgroup_delta": 0.1},
        safety={"harmful_rate": 0.1},
        drift={},
    )
    result = service.ci_check(request)
    assert result.status == "pass"
    assert result.violations == []


def test_config_file_adapter_reads_yaml(tmp_path: Path):
    config_data = {"foo": "bar"}
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.safe_dump(config_data))

    adapter = ConfigFileAdapter(cfg_path)
    assert adapter.load() == config_data


def test_config_file_adapter_invalid_yaml(tmp_path: Path):
    # Write invalid YAML content
    cfg_path = tmp_path / "invalid.yaml"
    cfg_path.write_text("foo: [unclosed_list\nbar: baz")

    adapter = ConfigFileAdapter(cfg_path)
    assert adapter.load() == {}


def test_config_file_adapter_invalid_json(tmp_path: Path):
    # Write invalid JSON content
    cfg_path = tmp_path / "invalid.json"
    cfg_path.write_text('{"foo": "bar", "baz": [1, 2,}')  # Invalid JSON

    adapter = ConfigFileAdapter(cfg_path)
    assert adapter.load() == {}


def test_config_file_adapter_handles_json(tmp_path: Path):
    config_data = {"foo": "bar"}
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(config_data))

    adapter = ConfigFileAdapter(cfg_path)
    assert adapter.load() == config_data


def test_config_file_adapter_missing_file(tmp_path: Path):
    adapter = ConfigFileAdapter(tmp_path / "missing.yaml")
    assert adapter.load() == {}
