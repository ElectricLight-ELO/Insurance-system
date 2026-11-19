from __future__ import annotations

from app.web_app.inspection_logic.domain.entities import DamageData, DamageAssessment
from app.web_app.inspection_logic.domain.errors import ValidationError
from app.web_app.inspection_logic.strategies.interfaces import DamageAssessmentStrategy


class InspectionLogic:
    """Контекст паттерна «Стратегия»: координирует расчёт ущерба."""

    def __init__(self, strategy: DamageAssessmentStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: DamageAssessmentStrategy) -> None:
        """Подмена алгоритма в рантайме."""
        self._strategy = strategy

    def assess(self, data: DamageData) -> DamageAssessment:
        self._validate(data)
        return self._strategy.calculate(data)

    def _validate(self, data: DamageData) -> None:
        if data.vehicle_age < 0:
            raise ValidationError("vehicle_age must be non-negative")
        if data.repair_cost < 0:
            raise ValidationError("repair_cost must be non-negative")
        if data.market_value <= 0:
            raise ValidationError("market_value must be positive")
        if data.photos_count < 0:
            raise ValidationError("photos_count must be non-negative")
