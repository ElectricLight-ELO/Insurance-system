from decimal import Decimal

from app.web_app.inspection_logic.domain.entities import DamageData, DamageAssessment
from app.web_app.inspection_logic.domain.enums import DamageCategory
from app.web_app.inspection_logic.strategies.interfaces import DamageAssessmentStrategy


class MinorDamageStrategy(DamageAssessmentStrategy):
    """Незначительный ущерб: выплата равна стоимости ремонта."""

    def calculate(self, data: DamageData) -> DamageAssessment:
        payout = data.repair_cost * Decimal("1.0")
        return DamageAssessment(
            category=DamageCategory.MINOR,
            payout=payout,
            requires_expert=False,
            requires_additional_photos=data.photos_count < 2,
        )
