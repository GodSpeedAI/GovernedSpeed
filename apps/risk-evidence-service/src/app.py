from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import os, json, time, hashlib, yaml

app = FastAPI(title="Risk & Evidence Service")

STORAGE = os.getenv("STORAGE_PATH", "/evidence")
CFG_PATH = os.getenv("PAC_CONFIG", "/config/adr-006.embedded-governance.yaml")

EVID_CNT = Counter("res_evidence_events_total", "Evidence events")
PASS5 = Gauge("llm_pass_at_5", "Quality pass@5")
FAIR = Gauge("fairness_subgroup_delta", "Fairness subgroup delta")
HARM = Gauge("harmful_output_rate", "Safety harmful rate")
DRIFT = Gauge("drift_psi", "Data drift PSI")
LAT95 = Gauge("latency_p95_seconds", "Latency p95 seconds")
AVAIL = Gauge("availability", "Availability")


def load_cfg():
    try:
        if CFG_PATH.endswith((".yml", ".yaml")):
            return yaml.safe_load(open(CFG_PATH))
        return json.load(open(CFG_PATH))
    except Exception:
        return {}


@app.get("/health")
def health():
    return {"status": "ok"}


class Evidence(BaseModel):
    artifactType: str
    modelVersion: str
    metadata: dict | None = None
    contentRef: str


@app.post("/evidence", status_code=201)
def evidence(ev: Evidence):
    EVID_CNT.inc()
    content = ev.model_dump()
    h = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    path = f"{STORAGE}/{int(time.time())}-{h}.json"
    os.makedirs(STORAGE, exist_ok=True)
    open(path, "w").write(json.dumps(content))
    return {
        "id": h,
        "evidence_hash": f"sha256:{h}",
        "stored_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/risk/snapshot")
def snapshot(model: str | None = None):
    # Simple demo snapshot; integrate your eval feeds here
    snap = {
        "model_version": model or "demo",
        "quality": {"pass_at_5": PASS5._value.get() or 0.84},
        "fairness": {"subgroup_delta": FAIR._value.get() or 0.03},
        "safety": {"harmful_rate": HARM._value.get() or 0.002},
        "privacy": {"reid_risk": 0.0006},
        "drift": {"psi": DRIFT._value.get() or 0.08},
        "eu_ai_act_tier": "Limited",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "evidence_hash": "sha256:demo",
    }
    return snap


class Incident(BaseModel):
    severity: str
    description: str
    refs: list[str] | None = None


@app.post("/incident", status_code=201)
def incident(body: Incident):
    h = hashlib.sha256(f"{time.time()}-{body.description}".encode()).hexdigest()
    return {
        "id": h,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "link": f"http://tickets/{h}",
    }
