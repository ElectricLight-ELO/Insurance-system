"""Слой API: приём REST-запросов по заявлениям о ДТП (AccidentController)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.schemas import ClaimCreateRequest, ClaimResponse, StatusChangeRequest
from app.dependencies import build_accident_service
from app.domain.entities import AccidentClaim
from app.services.interfaces import IAccidentService

router = APIRouter(prefix="/api/claims", tags=["Заявления о ДТП"])

AccidentServiceDep = Annotated[IAccidentService, Depends(build_accident_service)]


@router.post("", response_model=ClaimResponse, status_code=201, summary="Регистрация заявления о ДТП")
def register_claim(payload: ClaimCreateRequest, service: AccidentServiceDep) -> ClaimResponse:
    claim = AccidentClaim(
        number="",
        policy_number=payload.policy_number,
        region=payload.region,
        description=payload.description,
    )
    return ClaimResponse.from_claim(service.register_claim(claim))


@router.get("", response_model=list[ClaimResponse], summary="Список заявлений")
def list_claims(service: AccidentServiceDep) -> list[ClaimResponse]:
    return [ClaimResponse.from_claim(claim) for claim in service.list_claims()]


@router.get("/{claim_id}", response_model=ClaimResponse, summary="Карточка заявления и статус")
def get_claim(claim_id: UUID, service: AccidentServiceDep) -> ClaimResponse:
    return ClaimResponse.from_claim(service.get_claim(claim_id))


@router.post("/{claim_id}/assign", response_model=ClaimResponse, summary="Назначение аварийного эксперта")
def assign_expert(claim_id: UUID, service: AccidentServiceDep) -> ClaimResponse:
    return ClaimResponse.from_claim(service.assign_expert(claim_id))


@router.post("/{claim_id}/status", response_model=ClaimResponse, summary="Смена статуса заявления")
def change_status(claim_id: UUID, payload: StatusChangeRequest, service: AccidentServiceDep) -> ClaimResponse:
    return ClaimResponse.from_claim(service.change_status(claim_id, payload.status))
