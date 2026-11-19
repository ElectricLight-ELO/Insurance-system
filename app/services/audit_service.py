from __future__ import annotations

from uuid import UUID

from app.domain.entities import AuditEvent
from app.repositories.interfaces import IAccidentRepository


class AuditService:
    """Журналирование действий пользователей с системой."""

    def __init__(self, repo: IAccidentRepository) -> None:
        self._repo = repo

    def log(self, event: AuditEvent) -> None:
        self._repo.save_audit(event)

    def log_event(self, actor: str, action: str, entity_id: UUID) -> None:
        self.log(AuditEvent(actor=actor, action=action, entity_id=entity_id))
