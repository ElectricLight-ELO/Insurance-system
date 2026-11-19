from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
from .enums import DamageCategory


class InspectionCreateRequest(BaseModel):
    """POST /api/claims/{claim_id}/inspection — InspectionApiClient → InspectionController (как в коде Димы)."""
    damage_found: bool = Field(description="Зафиксированы ли повреждения")
    notes: str = Field(default="", description="Заключение эксперта")


class InspectionResponse(BaseModel):
    inspection_id: UUID
    claim_id: UUID
    expert_id: UUID
    damage_found: bool
    notes: str
    completed_at: datetime


class SignatureRequest(BaseModel):
    """POST /api/claims/{claim_id}/signature"""
    signed_by: str = Field(min_length=1, description="ФИО подписанта")


class SignatureResponse(BaseModel):
    signature_id: UUID
    claim_id: UUID
    signed_by: str
    verified: bool


class PhotosResponse(BaseModel):
    """POST /api/claims/{claim_id}/photos (multipart, поле files)"""
    photo_ids: list[UUID]


class DamageAssessmentDTO(BaseModel):
    """ПРЕДЛОЖЕНИЕ (J-03): результат InspectionLogic Никиты. Сейчас его клиент шлёт это тело
    на несуществующий POST /inspections. Вариант сшивки: вложить объект в InspectionCreateRequest.assessment."""
    category: DamageCategory
    payout: Decimal = Field(description="В JSON передаётся строкой, как делает клиент Никиты: str(payout)")
    requires_expert: bool
    requires_additional_photos: bool
