from enum import Enum


class DamageCategory(str, Enum):
    MINOR = "minor"
    MEDIUM = "medium"
    TOTAL_LOSS = "total_loss"
