from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities import TaskItem
from app.repositories.interfaces import IAccidentRepository


class ITaskQueue(ABC):
    """Очередь асинхронных задач (outbox)."""

    @abstractmethod
    def enqueue(self, task: TaskItem) -> UUID: ...


class TaskQueueFacade(ITaskQueue):
    """Постановка задач в очередь; демонстрационная имитация Worker'а."""

    def __init__(self, repo: IAccidentRepository) -> None:
        self._repo = repo

    def enqueue(self, task: TaskItem) -> UUID:
        task_id = self._repo.save_task(task)
        self._run_worker_demo(task)
        return task_id

    def _run_worker_demo(self, task: TaskItem) -> None:
        from app.worker import run_task_in_background

        run_task_in_background(task)
