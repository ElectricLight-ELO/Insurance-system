from __future__ import annotations

import sqlite3
from datetime import datetime
from uuid import UUID

from app.domain.entities import AccidentClaim, AuditEvent, Inspection, TaskItem
from app.domain.enums import AccidentStatus, TaskType
from app.repositories.interfaces import IAccidentRepository

_SCHEMA = """
CREATE TABLE IF NOT EXISTS claims (
    claim_id     TEXT PRIMARY KEY,
    number       TEXT NOT NULL,
    policy_number TEXT NOT NULL,
    region       TEXT NOT NULL,
    description  TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL,
    expert_id    TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inspections (
    inspection_id TEXT PRIMARY KEY,
    claim_id      TEXT NOT NULL,
    expert_id     TEXT NOT NULL,
    damage_found  INTEGER NOT NULL,
    notes         TEXT NOT NULL DEFAULT '',
    completed_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id    TEXT PRIMARY KEY,
    actor       TEXT NOT NULL,
    action      TEXT NOT NULL,
    entity_id   TEXT NOT NULL,
    occurred_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    task_id    TEXT PRIMARY KEY,
    type       TEXT NOT NULL,
    claim_id   TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS experts (
    expert_id TEXT PRIMARY KEY,
    name      TEXT NOT NULL,
    region    TEXT NOT NULL
);
"""

_SEED_EXPERTS: tuple[tuple[str, str, str], ...] = (
    ("11111111-1111-1111-1111-111111111111", "Иванов Иван Иванович", "Центральный"),
    ("22222222-2222-2222-2222-222222222222", "Петров Пётр Петрович", "Северный"),
    ("33333333-3333-3333-3333-333333333333", "Сидорова Светлана Сергеевна", "Центральный"),
    ("44444444-4444-4444-4444-444444444444", "Кузнецов Константин Игоревич", "Южный"),
)


class AccidentRepository(IAccidentRepository):
    """Реляционное хранилище (SQLAlchemy-совместимый диалект SQLite)."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._init_schema()

    def _init_schema(self) -> None:
        with self._connection:
            self._connection.executescript(_SCHEMA)
            self._connection.executemany(
                "INSERT OR IGNORE INTO experts (expert_id, name, region) VALUES (?, ?, ?)",
                _SEED_EXPERTS,
            )

    def get_claim(self, claim_id: UUID) -> AccidentClaim | None:
        row = self._connection.execute(
            """
            SELECT claim_id, number, policy_number, region, description,
                   status, expert_id, created_at
              FROM claims
             WHERE claim_id = ?
            """,
            (str(claim_id),),
        ).fetchone()
        return self._to_claim(row) if row else None

    def save_claim(self, claim: AccidentClaim) -> AccidentClaim:
        with self._connection:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO claims
                    (claim_id, number, policy_number, region, description,
                     status, expert_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(claim.claim_id),
                    claim.number,
                    claim.policy_number,
                    claim.region,
                    claim.description,
                    claim.status.value,
                    str(claim.expert_id) if claim.expert_id else None,
                    claim.created_at.isoformat(),
                ),
            )
        return claim

    def list_claims(self) -> list[AccidentClaim]:
        rows = self._connection.execute(
            """
            SELECT claim_id, number, policy_number, region, description,
                   status, expert_id, created_at
              FROM claims
             ORDER BY created_at DESC
            """
        ).fetchall()
        return [self._to_claim(row) for row in rows]

    def list_free_experts(self, region: str | None = None) -> list[UUID]:
        rows = self._connection.execute(
            """
            SELECT e.expert_id
              FROM experts e
             WHERE NOT EXISTS (
                       SELECT 1
                         FROM claims c
                        WHERE c.expert_id = e.expert_id
                          AND c.status != ?
                   )
               AND (? IS NULL OR e.region = ?)
             ORDER BY e.name
            """,
            (AccidentStatus.COMPLETED.value, region, region),
        ).fetchall()
        return [UUID(row["expert_id"]) for row in rows]

    def save_audit(self, event: AuditEvent) -> AuditEvent:
        with self._connection:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO audit_events
                    (event_id, actor, action, entity_id, occurred_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(event.event_id),
                    event.actor,
                    event.action,
                    str(event.entity_id),
                    event.occurred_at.isoformat(),
                ),
            )
        return event

    def save_task(self, task: TaskItem) -> UUID:
        with self._connection:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO tasks (task_id, type, claim_id, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(task.task_id),
                    task.type.value,
                    str(task.claim_id),
                    task.created_at.isoformat(),
                ),
            )
        return task.task_id

    def save_inspection(self, inspection: Inspection) -> Inspection:
        with self._connection:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO inspections
                    (inspection_id, claim_id, expert_id, damage_found, notes, completed_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(inspection.inspection_id),
                    str(inspection.claim_id),
                    str(inspection.expert_id),
                    1 if inspection.damage_found else 0,
                    inspection.notes,
                    inspection.completed_at.isoformat(),
                ),
            )
        return inspection

    def get_inspection(self, claim_id: UUID) -> Inspection | None:
        row = self._connection.execute(
            """
            SELECT inspection_id, claim_id, expert_id, damage_found, notes, completed_at
              FROM inspections
             WHERE claim_id = ?
            """,
            (str(claim_id),),
        ).fetchone()
        if row is None:
            return None
        return Inspection(
            claim_id=UUID(row["claim_id"]),
            expert_id=UUID(row["expert_id"]),
            damage_found=bool(row["damage_found"]),
            notes=row["notes"],
            inspection_id=UUID(row["inspection_id"]),
            completed_at=datetime.fromisoformat(row["completed_at"]),
        )

    @staticmethod
    def _to_claim(row: sqlite3.Row) -> AccidentClaim:
        return AccidentClaim(
            number=row["number"],
            policy_number=row["policy_number"],
            region=row["region"],
            description=row["description"],
            claim_id=UUID(row["claim_id"]),
            status=AccidentStatus(row["status"]),
            expert_id=UUID(row["expert_id"]) if row["expert_id"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
        )
