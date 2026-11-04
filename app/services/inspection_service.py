from __future__ import annotations

from uuid import UUID

from app.domain.entities import AccidentClaim, Inspection, Photo, Signature, TaskItem
from app.domain.enums import AccidentStatus, TaskType
from app.domain.errors import NotFoundError
from app.integration.ais_osago import IAisOsagoGateway
from app.integration.task_queue import ITaskQueue
from app.repositories.interfaces import IAccidentRepository, IFileRepository
from app.services.audit_service import AuditService
from app.services.interfaces import IInspectionService


class InspectionService(IInspectionService):
    """Бизнес-правила акта осмотра: фиксация повреждений, подпись, генерация протокола."""

    def __init__(
        self,
        claims: IAccidentRepository,
        files: IFileRepository,
        audit: AuditService,
        tasks: ITaskQueue,
        ais: IAisOsagoGateway,
    ) -> None:
        self._claims = claims
        self._files = files
        self._audit = audit
        self._tasks = tasks
        self._ais = ais

    def submit_results(self, inspection: Inspection) -> Inspection:
        claim = self._require_claim(inspection.claim_id)
        self._ais.check_policy(claim)
        claim.transition(AccidentStatus.INSPECTION)
        self._claims.save_claim(claim)
        saved = self._claims.save_inspection(inspection)
        self._audit.log_event(actor="expert", action="inspection_submitted", entity_id=saved.claim_id)
        return saved

    def upload_photos(self, claim_id: UUID, photos: list[bytes]) -> list[UUID]:
        self._require_claim(claim_id)
        entities = [Photo(content=content, meta=f"Фото осмотра заявления {claim_id}") for content in photos]
        saved_ids = self._files.save_photos(claim_id, entities)
        self._audit.log_event(actor="expert", action="photos_uploaded", entity_id=claim_id)
        return saved_ids

    def accept_signature(self, claim_id: UUID, signature: Signature) -> Signature:
        claim = self._require_claim(claim_id)
        signature.verified = True
        self._files.save_signature(claim_id, signature)
        self._tasks.enqueue(TaskItem(type=TaskType.PDF_PROTOCOL, claim_id=claim_id))
        claim.transition(AccidentStatus.COMPLETED)
        self._claims.save_claim(claim)
        self._audit.log_event(actor="client", action="protocol_signed", entity_id=claim_id)
        return signature

    def get_protocol(self, claim_id: UUID) -> bytes:
        self._require_claim(claim_id)
        content = self._files.get_pdf(claim_id)
        if content is None:
            raise NotFoundError("PDF-протокол ещё формируется (задача в очереди)")
        return content

    def _require_claim(self, claim_id: UUID) -> AccidentClaim:
        claim = self._claims.get_claim(claim_id)
        if claim is None:
            raise NotFoundError(f"Заявление {claim_id} не найдено")
        return claim
