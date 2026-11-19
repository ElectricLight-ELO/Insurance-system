"""Общие перечисления на стыках контейнеров. Значения 1:1 с кодом Димы (app/domain/enums.py)."""
from enum import Enum


class AccidentStatus(str, Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    INSPECTION = "inspection"
    COMPLETED = "completed"


class TaskType(str, Enum):
    """Типы задач в outbox (DB_AUDIT), которые API ставит, а Worker забирает."""
    PDF_PROTOCOL = "pdf_protocol"        # реализовано в коде Димы
    POLICY_RECHECK = "policy_recheck"    # реализовано в коде Димы
    REPORT = "report"                    # согласовано с Worker (ReportTask)
    MARGIN_CALC = "margin_calc"          # согласовано с Worker (MarginCalculationTask)
    CONTRACT_REG = "contract_reg"        # согласовано с Worker (RegistrationTask)
    EMAIL_SEND = "email_send"            # согласовано с Worker (NotificationTask)


class DamageCategory(str, Enum):
    """Категория ущерба (Никита, inspection_logic/domain/enums.py)."""
    MINOR = "minor"
    MEDIUM = "medium"
    TOTAL_LOSS = "total_loss"
