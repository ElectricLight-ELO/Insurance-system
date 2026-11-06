from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities import AccidentClaim, Inspection, Signature
from app.domain.enums import AccidentStatus


class IAccidentService(ABC):
    """Бизнес-логика заявления о ДТП."""

    @abstractmethod
    def register_claim(self, claim: AccidentClaim) -> AccidentClaim: ...

    @abstractmethod
    def assign_expert(self, claim_id: UUID) -> AccidentClaim: ...

    @abstractmethod
    def change_status(self, claim_id: UUID, status: AccidentStatus) -> AccidentClaim: ...

    @abstractmethod
    def get_claim(self, claim_id: UUID) -> AccidentClaim: ...

    @abstractmethod
    def list_claims(self) -> list[AccidentClaim]: ...


class IInspectionService(ABC):
    """Бизнес-логика акта осмотра и протокола."""

    @abstractmethod
    def submit_results(self, inspection: Inspection) -> Inspection: ...

    @abstractmethod
    def upload_photos(self, claim_id: UUID, photos: list[bytes]) -> list[UUID]: ...

    @abstractmethod
    def accept_signature(self, claim_id: UUID, signature: Signature) -> Signature: ...

    @abstractmethod
    def get_protocol(self, claim_id: UUID) -> bytes: ...
