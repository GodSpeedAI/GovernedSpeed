import sys
from pathlib import Path

from fastapi.testclient import TestClient


def _import_app():
    repo_root = Path(__file__).resolve().parents[3]
    src_dir = repo_root / "services" / "policy-gateway" / "src"
    sys.path.insert(0, str(src_dir))
    import app as gateway_app  # type: ignore

    return gateway_app


def test_proxy_streaming_sends_sse_chunks(monkeypatch):
    gateway_app = _import_app()

    class MockAdapter:
        def stream(self, request):
            yield "chunk-1"
            yield "chunk-2"

    # Patch the app's adapter factory to return our mock adapter
    monkeypatch.setattr(gateway_app, "_build_llm_adapter", lambda: MockAdapter())

    client = TestClient(gateway_app.app)

    resp = client.post("/proxy/completion/stream", json={"prompt": "hello"})
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers.get("content-type", "")
    text = resp.text
    # SSE events are prefixed with 'data: ' and separated by a blank line
    assert "data: chunk-1" in text
    assert "data: chunk-2" in text
