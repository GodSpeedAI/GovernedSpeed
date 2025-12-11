set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

pac_cfg := "libs/governance/policies/adr-006.embedded-governance.yaml"

# Nx commands
nx-graph:
    bunx nx graph

nx-build *ARGS:
    bunx nx run-many -t build {{ARGS}}

nx-test *ARGS:
    bunx nx run-many -t test {{ARGS}}

nx-lint *ARGS:
    bunx nx run-many -t lint {{ARGS}}

nx-affected *ARGS:
    bunx nx affected {{ARGS}}

ci-check:
    python3 tools/pac_ci.py \
      --config {{pac_cfg}} \
      --eval artifacts/eval_quality.json \
      --fairness artifacts/eval_fairness.json \
      --safety artifacts/eval_safety.json \
      --drift artifacts/eval_drift.json

deploy-config:
    kubectl apply -f deploy/policy-gateway/configmap.yaml

deploy-res:
    kubectl apply -f deploy/risk-evidence-service/secret.sample.yaml || true
    kubectl apply -f deploy/risk-evidence-service/deployment.yaml
    kubectl apply -f deploy/risk-evidence-service/service.yaml

deploy-vllm-with-gateway:
    helm upgrade --install policy-gateway ./deploy/policy-gateway \
      -f deploy/policy-gateway/values.yaml
    kubectl apply -f deploy/policy-gateway/service.yaml

dev-setup:
    # Creates/activates .venv and runs linter + tests via scripts/dev_setup.sh
    ./scripts/dev_setup.sh
