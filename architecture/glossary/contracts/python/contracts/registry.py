"""Реестр контрактов: статус и владелец. implemented — поля сверяются с кодом (verify_contracts.py)."""
from . import claims, inspection, tasks, auth_payment_admin as ap
from .enums import AccidentStatus, TaskType, DamageCategory

CONTRACTS = {
    "ClaimCreateRequest": (claims.ClaimCreateRequest, "implemented", "Дима"),
    "StatusChangeRequest": (claims.StatusChangeRequest, "implemented", "Дима"),
    "ClaimResponse": (claims.ClaimResponse, "implemented", "Дима"),
    "InspectionCreateRequest": (inspection.InspectionCreateRequest, "implemented", "Дима"),
    "InspectionResponse": (inspection.InspectionResponse, "implemented", "Дима"),
    "SignatureRequest": (inspection.SignatureRequest, "implemented", "Дима"),
    "SignatureResponse": (inspection.SignatureResponse, "implemented", "Дима"),
    "PhotosResponse": (inspection.PhotosResponse, "implemented", "Дима"),
    "DamageAssessmentDTO": (inspection.DamageAssessmentDTO, "proposed", "Никита"),
    "StoredDocument": (tasks.StoredDocument, "proposed", "Дима+Миша"),
    "OutboxTask": (tasks.OutboxTask, "proposed", "Дима+Миша"),
    "CodeRequest": (ap.CodeRequest, "proposed", "Дима"),
    "CodeVerifyRequest": (ap.CodeVerifyRequest, "proposed", "Дима"),
    "TokenResponse": (ap.TokenResponse, "proposed", "Дима"),
    "PaymentSessionRequest": (ap.PaymentSessionRequest, "proposed", "Дима"),
    "PaymentSessionResponse": (ap.PaymentSessionResponse, "proposed", "Дима"),
    "PaymentWebhook": (ap.PaymentWebhook, "proposed", "Дима"),
    "UserDTO": (ap.UserDTO, "proposed", "Дима+Амелия"),
    "TariffDTO": (ap.TariffDTO, "proposed", "Дима+Амелия"),
    "PolicyDTO": (ap.PolicyDTO, "proposed", "Дима+Амелия"),
    "PaymentDTO": (ap.PaymentDTO, "proposed", "Дима+Амелия"),
    "AuditEventDTO": (ap.AuditEventDTO, "proposed", "Дима+Амелия"),
    "MarginReportDTO": (ap.MarginReportDTO, "proposed", "Дима+Миша+Амелия"),
    "InvoiceRequest": (ap.InvoiceRequest, "proposed", "Дима+Амелия"),
    "TransactionRecord": (ap.TransactionRecord, "proposed", "Дима+Миша"),
    "TaskRestartRequest": (ap.TaskRestartRequest, "proposed", "Дима+Амелия"),
}
ENUMS = {"AccidentStatus": AccidentStatus, "TaskType": TaskType, "DamageCategory": DamageCategory}
