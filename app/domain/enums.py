from enum import Enum


class AccidentStatus(str, Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    INSPECTION = "inspection"
    COMPLETED = "completed"


class TaskType(str, Enum):
    PDF_PROTOCOL = "pdf_protocol"
    POLICY_RECHECK = "policy_recheck"
