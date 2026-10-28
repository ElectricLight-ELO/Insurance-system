from abc import ABC, abstractmethod

from app.web_app.inspection_logic.domain.entities import DamageData, DamageAssessment


class DamageAssessmentStrategy(ABC):
    """Контракт алгоритма оценки ущерба."""

    @abstractmethod
    def calculate(self, data: DamageData) -> DamageAssessment: ...
