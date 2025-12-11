from __future__ import annotations

import os
from typing import Dict

from fastapi import Depends, FastAPI
from policy_gateway.application.services import PolicyDecisionService
from policy_gateway.domain.models import (
    CiCheckInput,
    OutputDecisionInput,
    PromptDecisionInput,
)
from policy_gateway.infrastructure.config_file_adapter import ConfigFileAdapter
from policy_gateway.infrastructure.litellm_adapter import LiteLLMAdapter
from policy_gateway.infrastructure.llm_http_adapter import HTTPLLMAdapter
from policy_gateway.interface.http.schemas import (
    CiCheckRequest,
    CiCheckResponse,
    CompletionRequest,
    CompletionResponse,
    DecisionResponse,
    OutputCheckRequest,
    PromptCheckRequest,
)
from starlette.responses import StreamingResponse


def _build_service() -> PolicyDecisionService:
    cfg_path = os.getenv("PAC_CONFIG", "/config/adr-006.embedded-governance.yaml")
    configuration_adapter = ConfigFileAdapter(cfg_path)
    return PolicyDecisionService(configuration_adapter)


app = FastAPI(title="Policy Gateway")


def get_service() -> PolicyDecisionService:
    # Build a fresh service for each test/request to ensure environment
    # variables (like PAC_CONFIG) are picked up when tests monkeypatch them.
    return _build_service()


def _build_llm_adapter():
    """Factory for LLM adapters. Selects implementation using PAC_LLM_PROVIDER.

    Supported values for PAC_LLM_PROVIDER:
      - "litellm" -> LiteLLMAdapter (requires litellm package)
      - "http" (default) -> HTTPLLMAdapter
    """
    provider = os.getenv("PAC_LLM_PROVIDER", "http").lower()
    if provider == "litellm":
        # May raise if litellm is not installed — that's fine; surface as runtime error
        return LiteLLMAdapter()
    # default to HTTP forwarder
    return HTTPLLMAdapter()


@app.post("/proxy/completion", response_model=CompletionResponse)
def proxy_completion(
    body: CompletionRequest,
):
    adapter = _build_llm_adapter()
    # map HTTP request -> domain request
    from policy_gateway.domain.models import (
        CompletionRequest as DomainCompletionRequest,
    )

    domain_req = DomainCompletionRequest(
        prompt=body.prompt, model=body.model, max_tokens=body.max_tokens
    )
    result = adapter.complete(domain_req)
    return CompletionResponse(
        content=result.content, model=result.model, usage=result.usage
    )


@app.post("/proxy/completion/stream")
def proxy_completion_stream(body: CompletionRequest):
    """Stream completion results as Server-Sent-Events (SSE).

    The endpoint yields `data: <chunk>\n\n` for each chunk produced by the
    selected LLM adapter's stream() method.
    """
    adapter = _build_llm_adapter()
    from policy_gateway.domain.models import (
        CompletionRequest as DomainCompletionRequest,
    )

    domain_req = DomainCompletionRequest(
        prompt=body.prompt, model=body.model, max_tokens=body.max_tokens
    )

    def event_stream():
        for chunk in adapter.stream(domain_req):
            # SSE requires each event to be prefixed with `data:` and terminated by a blank line
            yield f"data: {chunk}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/health")
def health(service: PolicyDecisionService = Depends(get_service)) -> Dict[str, str]:
    return service.health()


@app.get("/rules")
def rules(service: PolicyDecisionService = Depends(get_service)) -> Dict[str, object]:
    return service.rules().to_dict()


@app.post("/filter/prompt", response_model=DecisionResponse)
def filter_prompt(
    body: PromptCheckRequest,
    service: PolicyDecisionService = Depends(get_service),
) -> DecisionResponse:
    decision = service.decide_prompt(
        PromptDecisionInput(prompt=body.prompt, context=body.context or {})
    )
    # Use centralized mapping from the domain model
    return DecisionResponse(**decision.to_response())


@app.post("/filter/output", response_model=DecisionResponse)
def filter_output(
    body: OutputCheckRequest,
    service: PolicyDecisionService = Depends(get_service),
) -> DecisionResponse:
    decision = service.decide_output(
        OutputDecisionInput(output=body.output, context=body.context or {})
    )
    return DecisionResponse(**decision.to_response())


@app.post("/ci/check", response_model=CiCheckResponse)
def ci_check(
    body: CiCheckRequest,
    service: PolicyDecisionService = Depends(get_service),
) -> CiCheckResponse:
    result = service.ci_check(
        CiCheckInput(
            quality=body.quality,
            fairness=body.fairness,
            safety=body.safety,
            drift=body.drift,
        )
    )
    return CiCheckResponse(**result.to_response())
