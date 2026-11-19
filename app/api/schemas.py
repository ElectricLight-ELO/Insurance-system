from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.entities import AccidentClaim, Inspection, Signature
from app.domain.enums import AccidentStatus


class ClaimCreateRequest(BaseModel):
    """Тело запроса регистрации заявления о ДТП."""

    policy_number: str = Field(min_length=1, description="Номер полиса ОСАГО, например ОСАГО-123456")
    region: str = Field(min_length=1, description="Регион ДТП, например Центральный")
    description: str = Field(default="", description="Описание обстоятельств ДТП")


class StatusChangeRequest(BaseModel):
    status: AccidentStatus


class ClaimResponse(BaseModel):
    claim_id: UUID
    number: str
    policy_number: str
    region: str
    description: str
    status: AccidentStatus
    expert_id: UUID | None = None
    created_at: datetime

    @classmethod
    def from_claim(cls, claim: AccidentClaim) -> ClaimResponse:
        return cls(
            claim_id=claim.claim_id,
            number=claim.number,
            policy_number=claim.policy_number,
            region=claim.region,
            description=claim.description,
            status=claim.status,
            expert_id=claim.expert_id,
            created_at=claim.created_at,
        )


class InspectionCreateRequest(BaseModel):
    damage_found: bool = Field(description="Зафиксированы ли повреждения")
    notes: str = Field(default="", description="Заключение эксперта")


class InspectionResponse(BaseModel):
    inspection_id: UUID
    claim_id: UUID
    expert_id: UUID
    damage_found: bool
    notes: str
    completed_at: datetime

    @classmethod
    def from_inspection(cls, inspection: Inspection) -> InspectionResponse:
        return cls(
            inspection_id=inspection.inspection_id,
            claim_id=inspection.claim_id,
            expert_id=inspection.expert_id,
            damage_found=inspection.damage_found,
            notes=inspection.notes,
            completed_at=inspection.completed_at,
        )


class SignatureRequest(BaseModel):
    signed_by: str = Field(min_length=1, description="ФИО подписанта")


class SignatureResponse(BaseModel):
    signature_id: UUID
    claim_id: UUID
    signed_by: str
    verified: bool

    @classmethod
    def from_signature(cls, signature: Signature) -> SignatureResponse:
        return cls(
            signature_id=signature.signature_id,
            claim_id=signature.claim_id,
            signed_by=signature.signed_by,
            verified=signature.verified,
        )


class PhotosResponse(BaseModel):
    photo_ids: list[UUID]
