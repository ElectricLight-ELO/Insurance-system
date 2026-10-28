"""CLI-демонстрация работы InspectionLogic (аналог main.py в FastAPI)."""

from __future__ import annotations

import logging
from decimal import Decimal

from app.web_app.inspection_logic.domain.entities import DamageData
from app.web_app.inspection_logic.domain.enums import DamageCategory
from app.web_app.inspection_logic.dependencies import build_inspection_logic_for_data
from app.web_app.inspection_logic.services.inspection_logic import InspectionLogic
from app.web_app.inspection_logic.strategies.medium_damage import MediumDamageStrategy
from app.web_app.inspection_logic.strategies.minor_damage import MinorDamageStrategy
from app.web_app.inspection_logic.strategies.total_loss import TotalLossStrategy

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main() -> None:
    data = DamageData(
        vehicle_age=3,
        repair_cost=Decimal("50000"),
        market_value=Decimal("800000"),
        photos_count=4,
        has_signature=True,
    )

    # 1. Явная подмена стратегий
    logic = InspectionLogic(MinorDamageStrategy())
    logging.info("Minor: %s", logic.assess(data))

    logic.set_strategy(MediumDamageStrategy())
    logging.info("Medium: %s", logic.assess(data))

    logic.set_strategy(TotalLossStrategy())
    logging.info("Total Loss: %s", logic.assess(data))

    # 2. Автоматический выбор через dependencies
    auto_logic = build_inspection_logic_for_data(data)
    logging.info("Auto: %s", auto_logic.assess(data))


if __name__ == "__main__":
    main()
