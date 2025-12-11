from __future__ import annotations

from typing import Any, Iterator

try:
    import litellm
except Exception:  # pragma: no cover - litellm may not be installed in analysis env
    litellm = None

from policy_gateway.domain.models import CompletionRequest, CompletionResponse
from policy_gateway.ports.llm_adapter import LLMAdapterPort


class LiteLLMAdapter(LLMAdapterPort):
    """Adapter that uses the `litellm` client when available.

    Notes:
    - We pass messages=[{"role":"user","content": ...}] to completion APIs
      since many litellm-like clients expect a messages structure.
    - All external client calls are wrapped to raise a clear RuntimeError from
      the original exception to preserve tracebacks and give callers a
      predictable adapter-level error type.
    """

    def __init__(self, model: str | None = None, **kwargs: Any) -> None:
        if litellm is None:
            raise RuntimeError("litellm package is not installed")
        self.model = model or "local"
        self._cfg: dict[str, Any] = kwargs

    def _extract_content_from_choice(self, choice: Any) -> str | None:
        # choice may be an object or a dict. Try standard shapes.
        msg = getattr(choice, "message", None) or (
            choice.get("message") if isinstance(choice, dict) else None
        )
        if msg:
            c = getattr(msg, "content", None) or (
                msg.get("content") if isinstance(msg, dict) else None
            )
            if c:
                return c

        delta = getattr(choice, "delta", None) or (
            choice.get("delta") if isinstance(choice, dict) else None
        )
        if isinstance(delta, dict):
            return delta.get("content")
        if delta is not None:
            return getattr(delta, "content", None)

        # fallback to top-level text on the choice
        return getattr(choice, "text", None) or (
            choice.get("text") if isinstance(choice, dict) else None
        )

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        # Prefer the completion() API with a messages list
        if hasattr(litellm, "completion"):
            try:
                resp = litellm.completion(
                    model=self.model,
                    messages=[{"role": "user", "content": request.prompt}],
                    max_tokens=request.max_tokens or None,
                    **self._cfg,
                )
            except Exception as e:
                raise RuntimeError("litellm completion failed") from e

            # try to extract content from choices or common fields
            choices = getattr(resp, "choices", None) or (
                resp.get("choices") if isinstance(resp, dict) else None
            )
            content = None
            if choices and len(choices) > 0:
                content = self._extract_content_from_choice(choices[0])

            if content is None:
                content = getattr(resp, "text", None) or (
                    resp.get("text") if isinstance(resp, dict) else None
                )
            if content is None:
                # Last resort, string-ify the response for diagnostics
                content = str(resp)

            model = getattr(resp, "model", None) or (
                resp.get("model") if isinstance(resp, dict) else self.model
            )
            usage = getattr(resp, "usage", None) or (
                resp.get("usage") if isinstance(resp, dict) else {}
            )
            return CompletionResponse(
                content=str(content), model=model, usage=usage or {}
            )

        # client-based API (older patterns)
        if hasattr(litellm, "Client"):
            try:
                client = litellm.Client(**self._cfg)
                resp = client.complete(
                    model=self.model,
                    messages=[{"role": "user", "content": request.prompt}],
                    max_tokens=request.max_tokens or None,
                )
            except Exception as e:
                raise RuntimeError("litellm client.complete failed") from e

            # Reuse same extraction logic
            choices = getattr(resp, "choices", None) or (
                resp.get("choices") if isinstance(resp, dict) else None
            )
            if choices and len(choices) > 0:
                text = self._extract_content_from_choice(choices[0])
            else:
                text = getattr(resp, "text", None) or (
                    resp.get("text") if isinstance(resp, dict) else str(resp)
                )

            return CompletionResponse(
                content=str(text),
                model=getattr(resp, "model", self.model),
                usage=getattr(resp, "usage", {}),
            )

        raise RuntimeError("No usable litellm completion API found")

    def stream(self, request: CompletionRequest) -> Iterator[str]:
        # Attempt to use the completion API with streaming enabled. Many
        # litellm-compatible clients return a generator when `stream=True`.
        if hasattr(litellm, "completion"):
            try:
                gen = litellm.completion(
                    model=self.model,
                    messages=[{"role": "user", "content": request.prompt}],
                    max_tokens=request.max_tokens or None,
                    stream=True,
                    **self._cfg,
                )
            except Exception:
                # Fall back to non-streaming single chunk on any error
                yield self.complete(request).content
                return

            try:
                for chunk in gen:
                    # chunk may be a string or an event-like object/dict
                    if isinstance(chunk, str):
                        if chunk:
                            yield chunk
                        continue

                    # extract choices -> delta/message content
                    choices = getattr(chunk, "choices", None) or (
                        chunk.get("choices") if isinstance(chunk, dict) else None
                    )
                    if choices and len(choices) > 0:
                        text = self._extract_content_from_choice(choices[0])
                        if text:
                            yield text
                return
            except Exception as e:
                # convert to domain-level adapter error
                raise RuntimeError("Error while iterating litellm stream") from e

        # Fallback — single chunk
        yield self.complete(request).content
