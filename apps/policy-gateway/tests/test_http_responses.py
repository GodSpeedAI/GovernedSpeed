from __future__ import annotations

from app import app as policy_app
from fastapi.testclient import TestClient
from policy_gateway.domain.models import CiCheckResult, DecisionResult
from policy_gateway.interface.http.schemas import CiCheckResponse, DecisionResponse


def test_decision_to_response_compatible_with_schema():
    dec = DecisionResult(allowed=True, action="safe_mode", reasons=["safe_content"])
    resp_dict = dec.to_response()
    resp = DecisionResponse(**resp_dict)
    assert resp.allowed is True
    assert resp.action == "safe_mode"
    assert resp.reasons == ["safe_content"]


def test_cicheck_to_response_compatible_with_schema():
    ci = CiCheckResult(status="fail", violations=["a", "b"])
    resp_dict = ci.to_response()
    resp = CiCheckResponse(**resp_dict)
    assert resp.status == "fail"
    assert resp.violations == ["a", "b"]


def test_filter_prompt_endpoint_returns_expected_shape():
    client = TestClient(policy_app)
    res = client.post("/filter/prompt", json={"prompt": "hello", "context": {}})
    assert res.status_code == 200
    body = res.json()
    # Ensure required keys exist
    assert set(body.keys()) >= {"allowed", "action", "reasons"}


def test_ci_check_endpoint_returns_expected_shape():
    client = TestClient(policy_app)
    payload = {"quality": {}, "fairness": {}, "safety": {}, "drift": {}}
    res = client.post("/ci/check", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert set(body.keys()) >= {"status", "violations"}
