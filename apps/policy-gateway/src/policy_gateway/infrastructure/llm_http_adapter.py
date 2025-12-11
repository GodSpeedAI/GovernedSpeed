from __future__ import annotations

import os
from typing import Dict

import httpx
from policy_gateway.domain.models import CompletionRequest, CompletionResponse
from policy_gateway.ports.llm_adapter import LLMAdapterPort


class HTTPLLMAdapter(LLMAdapterPort):
    """Simple HTTP-based LLM adapter that forwards completion requests to
    an upstream LLM endpoint (e.g., vLLM) defined by PAC_UPSTREAM_URL.

    This adapter keeps the contract small and easy to mock in tests. It sends
    JSON to the upstream and expects a JSON response with a `content` field.
    """

    def __init__(self, endpoint: str | None = None, timeout: int = 15):
        self.endpoint = endpoint or os.getenv(
            "PAC_UPSTREAM_URL", "http://localhost:8000"
        )
        self.timeout = timeout

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        url = self.endpoint.rstrip("/") + "/completion"
        payload: Dict[str, object] = {"prompt": request.prompt}
        if request.model:
            payload["model"] = request.model
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        try:
            resp = httpx.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            j = resp.json()
        except Exception as exc:  # keep broad for adapter boundary
            raise RuntimeError(f"LLM request failed: {exc}") from exc

        # Validate expected response shape: prefer `content` then `text`.
        if "content" in j and j.get("content") is not None:
            content = j.get("content")
        elif "text" in j and j.get("text") is not None:
            content = j.get("text")
        else:
            # Upstream returned an unexpected payload — include diagnostics
            body_snippet = resp.text if hasattr(resp, "text") else str(j)
            raise ValueError(
                f"Upstream LLM response missing 'content'/'text'; status={resp.status_code}, body={body_snippet[:1000]}"
            )

        return CompletionResponse(
            content=str(content), model=j.get("model"), usage=j.get("usage", {})
        )

    def stream(self, request: CompletionRequest):
        """Attempt to stream from the upstream LLM. If streaming isn't
        supported by the upstream, fall back to returning the completed
        response as a single chunk.
        """
        url = self.endpoint.rstrip("/") + "/completion"
        payload: Dict[str, object] = {"prompt": request.prompt}
        if request.model:
            payload["model"] = request.model
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        try:
            with httpx.stream("POST", url, json=payload, timeout=self.timeout) as resp:
                resp.raise_for_status()
                for chunk in resp.iter_text():
                    if chunk:
                        yield chunk
                return
        except Exception:
            # upstream doesn't support streaming or an error occurred; fall
            # back to a single completed chunk
            yield self.complete(request).content
