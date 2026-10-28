from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities import AccidentClaim, AuditEvent, Inspection, Photo, Signature, TaskItem


class IAccidentRepository(ABC):
    """Доступ к заявлениям о ДТП, актам осмотра, событиям аудита и очереди задач."""

    @abstractmethod
    def get_claim(self, claim_id: UUID) -> AccidentClaim | None: ...

    @abstractmethod
    def save_claim(self, claim: AccidentClaim) -> AccidentClaim: ...

    @abstractmethod
    def list_claims(self) -> list[AccidentClaim]: ...

    @abstractmethod
    def list_free_experts(self, region: str | None = None) -> list[UUID]: ...

    @abstractmethod
    def save_audit(self, event: AuditEvent) -> AuditEvent: ...

    @abstractmethod
    def save_task(self, task: TaskItem) -> UUID: ...

    @abstractmethod
    def save_inspection(self, inspection: Inspection) -> Inspection: ...

    @abstractmethod
    def get_inspection(self, claim_id: UUID) -> Inspection | None: ...


class IFileRepository(ABC):
    """Доступ к фото ДТП, подписям и PDF-документам."""

    @abstractmethod
    def save_photos(self, claim_id: UUID, photos: list[Photo]) -> list[UUID]: ...

    @abstractmethod
    def get_photos(self, claim_id: UUID) -> list[Photo]: ...

    @abstractmethod
    def save_signature(self, claim_id: UUID, signature: Signature) -> UUID: ...

    @abstractmethod
    def save_pdf(self, claim_id: UUID, content: bytes) -> UUID: ...

    @abstractmethod
    def get_pdf(self, claim_id: UUID) -> bytes | None: ...
