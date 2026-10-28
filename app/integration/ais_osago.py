from __future__ import annotations

import re
from abc import ABC, abstractmethod
from datetime import timedelta

from app.domain.entities import AccidentClaim, PolicyInfo
from app.domain.enums import TaskType
from app.domain.errors import IntegrationError

_POLICY_PATTERN = re.compile(r"^ОСАГО-\d{6}$")


class IAisOsagoGateway(ABC):
    """Шлюз к внешней системе АИС ОСАГО."""

    @abstractmethod
    def check_policy(self, claim: AccidentClaim) -> PolicyInfo: ...


class AisOsagoFacade(IAisOsagoGateway):
    """Изоляция внешнего вызова; в учебном проекте отвечает по формату полиса."""

    def __init__(self, base_url: str = "https://ais-osago.demo.example/api/v1") -> None:
        self._base_url = base_url

    def check_policy(self, claim: AccidentClaim) -> PolicyInfo:
        if not _POLICY_PATTERN.match(claim.policy_number):
            raise IntegrationError(
                f"Полис '{claim.policy_number}' не найден в АИС ОСАГО "
                "(ожидается формат ОСАГО-XXXXXX)"
            )
        return PolicyInfo(
            number=claim.policy_number,
            is_valid=True,
            expires_at=claim.created_at + timedelta(days=365),
        )
