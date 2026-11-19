from decimal import Decimal

import pytest

from app.web_app.inspection_logic.domain.entities import DamageData
from app.web_app.inspection_logic.domain.enums import DamageCategory
from app.web_app.inspection_logic.domain.errors import ValidationError
from app.web_app.inspection_logic.services.inspection_logic import InspectionLogic
from app.web_app.inspection_logic.strategies.minor_damage import MinorDamageStrategy
from app.web_app.inspection_logic.strategies.total_loss import TotalLossStrategy


@pytest.fixture
def data() -> DamageData:
    return DamageData(
        vehicle_age=3,
        repair_cost=Decimal("50000"),
        market_value=Decimal("800000"),
        photos_count=4,
        has_signature=True,
    )


def test_minor_strategy(data: DamageData) -> None:
    logic = InspectionLogic(MinorDamageStrategy())
    result = logic.assess(data)
    assert result.category == DamageCategory.MINOR
    assert result.payout == Decimal("50000.0")
    assert result.requires_expert is False


def test_strategy_swap(data: DamageData) -> None:
    logic = InspectionLogic(MinorDamageStrategy())
    logic.set_strategy(TotalLossStrategy())
    result = logic.assess(data)
    assert result.category == DamageCategory.TOTAL_LOSS
    assert result.requires_expert is True


def test_validation_negative_age() -> None:
    logic = InspectionLogic(MinorDamageStrategy())
    bad_data = DamageData(
        vehicle_age=-1,
        repair_cost=Decimal("50000"),
        market_value=Decimal("800000"),
        photos_count=4,
        has_signature=True,
    )
    with pytest.raises(ValidationError):
        logic.assess(bad_data)
