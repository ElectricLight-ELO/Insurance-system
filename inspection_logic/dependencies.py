"""Сборка зависимостей для InspectionLogic (аналог DI в FastAPI)."""

from __future__ import annotations

from app.web_app.inspection_logic.domain.enums import DamageCategory
from app.web_app.inspection_logic.domain.entities import DamageData
from app.web_app.inspection_logic.services.inspection_logic import InspectionLogic
from app.web_app.inspection_logic.strategies.interfaces import DamageAssessmentStrategy
from app.web_app.inspection_logic.strategies.minor_damage import MinorDamageStrategy
from app.web_app.inspection_logic.strategies.medium_damage import MediumDamageStrategy
from app.web_app.inspection_logic.strategies.total_loss import TotalLossStrategy


def get_strategy_for_category(category: DamageCategory) -> DamageAssessmentStrategy:
    """Фабрика стратегий (Factory Method)."""
    if category == DamageCategory.MINOR:
        return MinorDamageStrategy()
    if category == DamageCategory.MEDIUM:
        return MediumDamageStrategy()
    return TotalLossStrategy()


def build_inspection_logic_for_data(data: DamageData) -> InspectionLogic:
    """Автоматический выбор стратегии по бизнес-правилу."""
    # Пример правила: если ремонт < 30% рыночной стоимости — minor, < 70% — medium, иначе total_loss
    if data.repair_cost < data.market_value * Decimal("0.3"):
        strategy = MinorDamageStrategy()
    elif data.repair_cost < data.market_value * Decimal("0.7"):
        strategy = MediumDamageStrategy()
    else:
        strategy = TotalLossStrategy()
    return InspectionLogic(strategy)
