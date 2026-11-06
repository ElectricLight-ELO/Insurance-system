from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import AccidentStatus, TaskType


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> UUID:
    return uuid4()


@dataclass
class AccidentClaim:
    number: str
    policy_number: str
    region: str
    description: str = ""
    claim_id: UUID = field(default_factory=_uuid)
    status: AccidentStatus = AccidentStatus.NEW
    expert_id: UUID | None = None
    created_at: datetime = field(default_factory=_now)

    def assign(self, expert_id: UUID) -> None:
        self.expert_id = expert_id
        self.status = AccidentStatus.ASSIGNED

    def transition(self, status: AccidentStatus) -> None:
        self.status = status


@dataclass
class Inspection:
    claim_id: UUID
    expert_id: UUID
    damage_found: bool
    notes: str
    inspection_id: UUID = field(default_factory=_uuid)
    completed_at: datetime = field(default_factory=_now)


@dataclass
class Photo:
    content: bytes
    meta: str = ""
    photo_id: UUID = field(default_factory=_uuid)


@dataclass
class Signature:
    claim_id: UUID
    signed_by: str
    content: bytes
    signature_id: UUID = field(default_factory=_uuid)
    verified: bool = False


@dataclass
class AuditEvent:
    actor: str
    action: str
    entity_id: UUID
    event_id: UUID = field(default_factory=_uuid)
    occurred_at: datetime = field(default_factory=_now)


@dataclass
class TaskItem:
    type: TaskType
    claim_id: UUID
    task_id: UUID = field(default_factory=_uuid)
    created_at: datetime = field(default_factory=_now)


@dataclass
class PolicyInfo:
    number: str
    is_valid: bool
    expires_at: datetime
