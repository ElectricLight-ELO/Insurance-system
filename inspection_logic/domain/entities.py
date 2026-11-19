from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.web_app.inspection_logic.domain.enums import DamageCategory


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class DamageData:
    """Входные данные осмотра (value object)."""
    vehicle_age: int
    repair_cost: Decimal
    market_value: Decimal
    photos_count: int
    has_signature: bool


@dataclass(frozen=True)
class DamageAssessment:
    """Результат оценки ущерба (value object)."""
    category: DamageCategory
    payout: Decimal
    requires_expert: bool
    requires_additional_photos: bool
    assessment_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=_now)


@dataclass(frozen=True)
class AssessmentResponse:
    """Ответ от API после отправки оценки."""
    assessment_id: UUID
    accepted: bool
    server_message: str
