from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from .enums import AccidentStatus


class ClaimCreateRequest(BaseModel):
    """POST /api/claims — AccidentApiClient → AccidentController."""
    policy_number: str = Field(min_length=1, description="Номер полиса ОСАГО, например ОСАГО-123456")
    region: str = Field(min_length=1, description="Регион ДТП, например Центральный")
    description: str = Field(default="", description="Описание обстоятельств ДТП")


class StatusChangeRequest(BaseModel):
    """POST /api/claims/{claim_id}/status"""
    status: AccidentStatus


class ClaimResponse(BaseModel):
    claim_id: UUID
    number: str
    policy_number: str
    region: str
    description: str
    status: AccidentStatus
    expert_id: UUID | None = None
    created_at: datetime
