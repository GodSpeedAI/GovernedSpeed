import sys
from pathlib import Path

from fastapi.testclient import TestClient


def _import_app():
    # Ensure service src is on sys.path so imports work in CI and local runs
    repo_root = Path(__file__).resolve().parents[3]
    src_dir = repo_root / "services" / "policy-gateway" / "src"
    sys.path.insert(0, str(src_dir))
    import app as gateway_app  # type: ignore

    return gateway_app.app


def test_filter_prompt_and_ci_check(tmp_path, monkeypatch):
    # prepare a minimal config with thresholds
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text(
        """
thresholds:
  quality:
    pass_at_5:
      target: 0.82
"""
    )

    monkeypatch.setenv("PAC_CONFIG", str(cfg))

    app = _import_app()
    client = TestClient(app)

    # prompt filter: high jailbreak score should trigger safe_mode
    resp = client.post(
        "/filter/prompt", json={"prompt": "hello", "context": {"jailbreak_score": 0.9}}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("allowed") is True
    assert body.get("action") == "safe_mode"
    assert "high jailbreak score" in (body.get("reasons") or [])

    # ci check: below threshold should fail
    ci_payload = {
        "quality": {"pass_at_5": 0.8},
        "fairness": {"subgroup_delta": 0.01},
        "safety": {"harmful_rate": 0.0},
        "drift": {},
    }
    resp2 = client.post("/ci/check", json=ci_payload)
    assert resp2.status_code == 200
    r2 = resp2.json()
    assert r2.get("status") == "fail"
    assert "quality.pass_at_5" in r2.get("violations", [])

    # now pass case
    ci_payload["quality"]["pass_at_5"] = 0.85
    resp3 = client.post("/ci/check", json=ci_payload)
    assert resp3.status_code == 200
    r3 = resp3.json()
    assert r3.get("status") == "pass"
