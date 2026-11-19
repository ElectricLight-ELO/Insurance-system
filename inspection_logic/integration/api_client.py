from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.web_app.inspection_logic.domain.entities import DamageAssessment, AssessmentResponse
from app.web_app.inspection_logic.domain.errors import IntegrationError


class IHttpClient(ABC):
    """Абстракция HTTP-клиента (DIP)."""

    @abstractmethod
    def post(self, url: str, json: dict) -> dict: ...


class InspectionApiClient:
    """Клиент для отправки результатов оценки на бэкенд."""

    def __init__(self, base_url: str, http: IHttpClient) -> None:
        self._base_url = base_url
        self._http = http

    def submit_results(self, assessment: DamageAssessment) -> AssessmentResponse:
        payload = {
            "category": assessment.category.value,
            "payout": str(assessment.payout),
            "requires_expert": assessment.requires_expert,
            "requires_additional_photos": assessment.requires_additional_photos,
        }
        try:
            raw = self._http.post(f"{self._base_url}/inspections", payload)
        except Exception as error:
            raise IntegrationError(f"Не удалось отправить оценку: {error}") from error

        return AssessmentResponse(
            assessment_id=UUID(raw["id"]),
            accepted=raw["accepted"],
            server_message=raw["message"],
        )
