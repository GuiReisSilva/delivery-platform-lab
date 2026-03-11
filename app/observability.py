from __future__ import annotations

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter, Histogram,
    generate_latest
)

release_requests_total = Counter(
    "release_requests_total",
    "Total release requests",
    ["service"],
)

release_duration_seconds = Histogram(
    "release_duration_seconds",
    "Time spent processing a release",
    ["service"],
)

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["path", "method", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["path", "method"],
)


def metrics_payload() -> tuple[bytes, str]:
    body = generate_latest()
    return body, CONTENT_TYPE_LATEST
