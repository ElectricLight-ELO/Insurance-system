"""ПРЕДЛОЖЕННЫЕ контракты (кода у команды пока нет, поэтому статус proposed). Нужны, чтобы Web App/Backoffice и API
сверяли поля по одному описанию."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class CodeRequest(BaseModel):
    """POST /api/auth/code — запрос одноразового кода (AuthApiClient → AuthController → SmsGatewayFacade)."""
    phone: str = Field(min_length=5)


class CodeVerifyRequest(BaseModel):
    """POST /api/auth/verify"""
    phone: str = Field(min_length=5)
    code: str = Field(min_length=4, max_length=8)


class TokenResponse(BaseModel):
    access_token: str
    role: str
    expires_at: datetime


class PaymentSessionRequest(BaseModel):
    """POST /api/payments/session (PolicyApiClient → PaymentController)"""
    policy_id: UUID
    amount: Decimal


class PaymentSessionResponse(BaseModel):
    session_id: str
    pay_url: str


class PaymentWebhook(BaseModel):
    """POST /api/payments/webhook (Платёжная система → PaymentController)"""
    session_id: str
    status: str
    amount: Decimal


class UserDTO(BaseModel):
    """GET/POST /api/admin/users (AdminApiClient → AdminController)"""
    user_id: UUID
    full_name: str
    role: str
    active: bool = True


class TariffDTO(BaseModel):
    """GET/PUT /api/admin/tariffs"""
    tariff_id: UUID
    region: str
    base_rate: Decimal
    coefficient: Decimal


class TaskRestartRequest(BaseModel):
    """POST /api/admin/tasks/{task_id}/restart (OperationsApiClient → AdminController → TaskQueueFacade)"""
    reason: str = ""


class PolicyDTO(BaseModel):
    """GET /api/admin/policies (OperationsApiClient → AdminController): поиск полисов"""
    policy_number: str
    holder: str
    status: str
    expires_at: datetime


class PaymentDTO(BaseModel):
    """GET /api/admin/payments, /api/admin/finance/payments: статусы платежей"""
    payment_id: UUID
    policy_number: str
    amount: Decimal
    status: str
    paid_at: datetime | None = None


class AuditEventDTO(BaseModel):
    """GET /api/admin/audit (AuditApiClient → AdminController): журнал аудита"""
    event_id: UUID
    actor: str
    action: str
    entity_id: UUID
    occurred_at: datetime


class MarginReportDTO(BaseModel):
    """Результат расчёта маржи: Worker пишет в DB_TARIFS, API отдаёт FinanceApiClient (GET /api/admin/finance/margin)"""
    period_start: datetime
    period_end: datetime
    revenue: Decimal
    commission: Decimal
    margin: Decimal


class InvoiceRequest(BaseModel):
    """POST /api/admin/finance/invoices (FinanceApiClient → AdminController → задача REPORT)"""
    period_start: datetime
    period_end: datetime


class TransactionRecord(BaseModel):
    """Запись о транзакции в DB_AUDIT: пишет API (AccidentRepository), читает Worker (TransactionRepository)"""
    transaction_id: UUID
    policy_number: str
    amount: Decimal
    status: str
    created_at: datetime
