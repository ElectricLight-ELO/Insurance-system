from decimal import Decimal

from app.web_app.inspection_logic.domain.entities import DamageData, DamageAssessment
from app.web_app.inspection_logic.domain.enums import DamageCategory
from app.web_app.inspection_logic.strategies.interfaces import DamageAssessmentStrategy


class TotalLossStrategy(DamageAssessmentStrategy):
    """Полная гибель ТС: выплата = рыночная стоимость × 0.85, всегда нужен эксперт."""

    def calculate(self, data: DamageData) -> DamageAssessment:
        payout = data.market_value * Decimal("0.85")
        return DamageAssessment(
            category=DamageCategory.TOTAL_LOSS,
            payout=payout,
            requires_expert=True,
            requires_additional_photos=not data.has_signature,
        )
