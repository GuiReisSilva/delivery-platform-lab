from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass
class Release:
    id: str
    service: str
    version: str
    status: str
    steps: List[str]
    created_at: float


class ReleaseStore:
    def __init__(self) -> None:
        self._items: Dict[str, Release] = {}

    def create(self, service: str, version: str) -> Release:
        rid = str(uuid.uuid4())
        rel = Release(
            id=rid,
            service=service,
            version=version,
            status="created",
            steps=[],
            created_at=time.time(),
        )
        self._items[rid] = rel
        return rel

    def update(self, rid: str, status: str, step: str | None = None) -> Release:
        rel = self._items[rid]
        rel.status = status
        if step:
            rel.steps.append(step)
        self._items[rid] = rel
        return rel

    def list(self) -> List[dict]:
        return [
            asdict(r)
            for r in sorted(self._items.values(), 
                            key=lambda x: x.created_at,
                            reverse=True)] 
    
    def get(self, rid: str):
        return self._items.get(rid)
