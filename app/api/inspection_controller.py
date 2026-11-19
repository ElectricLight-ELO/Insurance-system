"""Слой API: приём REST-запросов по результатам осмотра (InspectionController)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response

from app.api.accident_controller import AccidentServiceDep
from app.api.schemas import (
    InspectionCreateRequest,
    InspectionResponse,
    PhotosResponse,
    SignatureRequest,
    SignatureResponse,
)
from app.dependencies import build_inspection_service
from app.domain.entities import Inspection, Signature
from app.domain.errors import NotFoundError
from app.services.interfaces import IInspectionService

router = APIRouter(prefix="/api/claims", tags=["Осмотр и протокол"])

InspectionServiceDep = Annotated[IInspectionService, Depends(build_inspection_service)]


@router.post(
    "/{claim_id}/inspection",
    response_model=InspectionResponse,
    summary="Приём результатов осмотра",
)
def submit_results(
    claim_id: UUID,
    payload: InspectionCreateRequest,
    service: InspectionServiceDep,
    accident: AccidentServiceDep,
) -> InspectionResponse:
    claim = accident.get_claim(claim_id)
    if claim.expert_id is None:
        raise HTTPException(status_code=409, detail="Эксперт ещё не назначен")
    inspection = Inspection(
        claim_id=claim_id,
        expert_id=claim.expert_id,
        damage_found=payload.damage_found,
        notes=payload.notes,
    )
    return InspectionResponse.from_inspection(service.submit_results(inspection))


@router.post(
    "/{claim_id}/photos",
    response_model=PhotosResponse,
    summary="Загрузка фотографий осмотра",
)
async def upload_photos(
    claim_id: UUID,
    service: InspectionServiceDep,
    files: Annotated[list[UploadFile], File(description="Фотографии места ДТП")],
) -> PhotosResponse:
    photos = [await file.read() for file in files]
    photo_ids = service.upload_photos(claim_id, photos)
    return PhotosResponse(photo_ids=photo_ids)

@router.post(
    "/{claim_id}/signature",
    response_model=SignatureResponse,
    summary="Приём электронной подписи клиента",
)
def accept_signature(claim_id: UUID, payload: SignatureRequest, service: InspectionServiceDep) -> SignatureResponse:
    signature = Signature(
        claim_id=claim_id,
        signed_by=payload.signed_by,
        content=payload.signed_by.encode("utf-8"),
    )
    return SignatureResponse.from_signature(service.accept_signature(claim_id, signature))


@router.get(
    "/{claim_id}/protocol",
    summary="PDF-протокол осмотра",
)
def get_protocol(claim_id: UUID, service: InspectionServiceDep) -> Response:
    try:
        content = service.get_protocol(claim_id)
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="protocol-{claim_id}.pdf"'},
    )
