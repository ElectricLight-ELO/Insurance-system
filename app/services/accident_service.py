from __future__ import annotations

from uuid import UUID

from app.domain.entities import AccidentClaim
from app.domain.enums import AccidentStatus
from app.domain.errors import NotFoundError
from app.repositories.interfaces import IAccidentRepository
from app.services.audit_service import AuditService
from app.services.interfaces import IAccidentService
from app.strategies.assignment import AssignmentStrategy


class AccidentService(IAccidentService):
    """Бизнес-правила заявления о ДТП: создание, назначение эксперта, смена статусов."""

    def __init__(
        self,
        repo: IAccidentRepository,
        audit: AuditService,
        assignment: AssignmentStrategy,
    ) -> None:
        self._repo = repo
        self._audit = audit
        self._assignment = assignment

    def register_claim(self, claim: AccidentClaim) -> AccidentClaim:
        if not claim.number:
            claim.number = f"ДТП-{len(self._repo.list_claims()) + 1:04d}"
        saved = self._repo.save_claim(claim)
        self._audit.log_event(actor="dispatcher", action="claim_registered", entity_id=saved.claim_id)
        return saved

    def assign_expert(self, claim_id: UUID) -> AccidentClaim:
        claim = self._require_claim(claim_id)
        expert_id = self._assignment.select_expert(claim)
        claim.assign(expert_id)
        saved = self._repo.save_claim(claim)
        self._audit.log_event(actor="dispatcher", action="expert_assigned", entity_id=saved.claim_id)
        return saved

    def change_status(self, claim_id: UUID, status: AccidentStatus) -> AccidentClaim:
        claim = self._require_claim(claim_id)
        claim.transition(status)
        saved = self._repo.save_claim(claim)
        self._audit.log_event(actor="system", action="status_changed", entity_id=saved.claim_id)
        return saved

    def get_claim(self, claim_id: UUID) -> AccidentClaim:
        return self._require_claim(claim_id)

    def list_claims(self) -> list[AccidentClaim]:
        return self._repo.list_claims()

    def _require_claim(self, claim_id: UUID) -> AccidentClaim:
        claim = self._repo.get_claim(claim_id)
        if claim is None:
            raise NotFoundError(f"Заявление {claim_id} не найдено")
        return claim
