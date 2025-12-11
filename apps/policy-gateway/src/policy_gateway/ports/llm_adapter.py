from __future__ import annotations

from typing import Iterator, Protocol

from policy_gateway.domain.models import CompletionRequest, CompletionResponse


class LLMAdapterPort(Protocol):
    """Abstract port for LLM adapters used by the Policy Gateway.

    Methods:
      - complete(request) -> CompletionResponse: return the final completion.
      - stream(request) -> Iterator[str]: yield text chunks from the model.

    The stream() method may yield a single element if the provider doesn't
    support streaming; callers should treat it as a streaming API.
    """

    def complete(self, request: CompletionRequest) -> CompletionResponse: ...

    def stream(self, request: CompletionRequest) -> Iterator[str]: ...
