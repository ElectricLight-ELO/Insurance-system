from __future__ import annotations

import logging
import sqlite3
import threading

from app.config import DB_PATH, STORAGE_DIR
from app.domain.entities import TaskItem
from app.domain.enums import TaskType
from app.integration.pdf_protocol import build_protocol_pdf
from app.repositories.accident_repository import AccidentRepository
from app.repositories.file_repository import FileRepository
from app.repositories.interfaces import IAccidentRepository, IFileRepository

logger = logging.getLogger(__name__)


def process_task(task: TaskItem, claims: IAccidentRepository, files: IFileRepository) -> None:
    """Выполнение фоновой задачи (демонстрационная замена Worker/Celery)."""
    if task.type is TaskType.PDF_PROTOCOL:
        claim = claims.get_claim(task.claim_id)
        if claim is None:
            logger.warning("Заявление %s не найдено, задача %s отменена", task.claim_id, task.task_id)
            return
        inspection = claims.get_inspection(task.claim_id)
        photos_count = len(files.get_photos(task.claim_id))
        files.save_pdf(task.claim_id, build_protocol_pdf(claim, inspection, photos_count))
        logger.info("PDF-протокол по заявлению %s сформирован", claim.number)


def run_task_in_background(task: TaskItem) -> None:
    """Запуск задачи в отдельном потоке со своим подключением к БД."""

    def execute() -> None:
        connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        try:
            process_task(task, AccidentRepository(connection), FileRepository(STORAGE_DIR))
        except Exception:
            logger.exception("Ошибка выполнения задачи %s", task.task_id)
        finally:
            connection.close()

    threading.Thread(target=execute, daemon=True).start()
