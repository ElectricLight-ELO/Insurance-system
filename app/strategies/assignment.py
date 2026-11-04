from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities import AccidentClaim
from app.domain.errors import DomainError
from app.repositories.interfaces import IAccidentRepository


class AssignmentStrategy(ABC):
    """Алгоритм назначения аварийного эксперта на заявление о ДТП."""

    def __init__(self, repo: IAccidentRepository) -> None:
        self._repo = repo

    @abstractmethod
    def select_expert(self, claim: AccidentClaim) -> UUID: ...


class FreeExpertStrategy(AssignmentStrategy):
    """Назначает первого свободного эксперта независимо от региона."""

    def select_expert(self, claim: AccidentClaim) -> UUID:
        free_experts = self._repo.list_free_experts(None)
        if not free_experts:
            raise DomainError("Нет свободных аварийных экспертов")
        return free_experts[0]


class RegionExpertStrategy(AssignmentStrategy):
    """Назначает свободного эксперта того же региона, где произошло ДТП."""

    def select_expert(self, claim: AccidentClaim) -> UUID:
        local_experts = self._repo.list_free_experts(claim.region)
        if local_experts:
            return local_experts[0]
        any_experts = self._repo.list_free_experts(None)
        if not any_experts:
            raise DomainError("Нет свободных аварийных экспертов")
        return any_experts[0]
