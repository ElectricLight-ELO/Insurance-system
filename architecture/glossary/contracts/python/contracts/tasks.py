from __future__ import annotations
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel
from .enums import TaskType


class OutboxStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class OutboxTask(BaseModel):
    """Запись очереди в DB_AUDIT (outbox). API: TaskQueueFacade → AccidentRepository. Worker: OutboxPoller → AuditRepository.
    Поля type/claim_id/task_id/created_at совпадают с TaskItem из кода Димы; status/attempts/error — ПРЕДЛОЖЕНИЕ (J-11)."""
    task_id: UUID
    type: TaskType
    claim_id: UUID | None = None
    created_at: datetime
    status: OutboxStatus = OutboxStatus.PENDING
    attempts: int = 0
    error: str | None = None


class StoredDocument(BaseModel):
    """ПРЕДЛОЖЕНИЕ (J-13): запись в DB_FILES. API пишет photo/signature, Worker читает их и пишет pdf."""
    claim_id: UUID
    kind: str  # photo | signature | pdf
    file_id: UUID
    created_at: datetime
