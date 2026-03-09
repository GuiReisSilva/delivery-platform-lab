from __future__ import annotations

import time

import logging
import structlog
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.observability import (
    metrics_payload,
    release_duration_seconds,
    release_requests_total,
)
from app.release_service import ReleaseStore

logging.basicConfig(level=logging.INFO)

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

logger = structlog.get_logger()

app = FastAPI(title="Delivery Platform Lab", version="0.1.0")
store = ReleaseStore()


class ReleaseRequest(BaseModel):
    service: str = Field(min_length=2, max_length=50)
    version: str = Field(min_length=1, max_length=30)


@app.get("/")
def root():
    return {"app": "delivery-platform-lab"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/live")
def live():
    return {"status": "alive"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/releases")
def list_releases():
    return {"items": store.list()}


@app.post("/release")
def create_release(payload: ReleaseRequest):
    t0 = time.time()
    rel = store.create(payload.service, payload.version)

    steps = ["build", "test", "deploy"]
    release_requests_total.labels(service=payload.service).inc()

    with release_duration_seconds.labels(service=payload.service).time():
        for step in steps:
            logger.info(
                "release_step",
                release_id=rel.id,
                service=payload.service,
                version=payload.version,
                step=step,
            )
            store.update(rel.id, status=f"running:{step}", step=step)
            time.sleep(0.5)

        store.update(rel.id, status="done")

    logger.info(
        "release_done",
        release_id=rel.id,
        service=payload.service,
        version=payload.version,
        elapsed=time.time() - t0,
    )
    return {"release_id": rel.id, "status": "done"}


@app.get("/release/{rid}")
def get_release(rid: str):
    rel = store.get(rid)
    if not rel:
        return {"error": "release not found"}
    return rel


@app.get("/metrics")
def metrics():
    body, content_type = metrics_payload()
    return Response(content=body, media_type=content_type)
