"""Пакет contracts — единственное описание данных на стыках контейнеров ИС ОСАГО.
Python-модели (Pydantic) — источник истины; TypeScript-типы генерируются: python ../../gen_ts.py"""
from .enums import AccidentStatus, TaskType, DamageCategory
from .claims import *
from .inspection import *
from .tasks import *
from .auth_payment_admin import *
