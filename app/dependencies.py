"""Композиционный корень: сборка зависимостей по принципу DIP."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Query

from app.config import DB_PATH, STORAGE_DIR
from app.integration.ais_osago import AisOsagoFacade, IAisOsagoGateway
from app.integration.task_queue import ITaskQueue, TaskQueueFacade
from app.repositories.accident_repository import AccidentRepository
from app.repositories.file_repository import FileRepository
from app.repositories.interfaces import IAccidentRepository, IFileRepository
from app.services.accident_service import AccidentService
from app.services.audit_service import AuditService
from app.services.inspection_service import InspectionService
from app.services.interfaces import IAccidentService, IInspectionService
from app.strategies.assignment import AssignmentStrategy, FreeExpertStrategy, RegionExpertStrategy


def get_connection() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def get_claims_repository(
    connection: sqlite3.Connection = Depends(get_connection),
) -> IAccidentRepository:
    return AccidentRepository(connection)


def get_files_repository() -> IFileRepository:
    return FileRepository(STORAGE_DIR)


def get_audit_service(
    claims: IAccidentRepository = Depends(get_claims_repository),
) -> AuditService:
    return AuditService(claims)


def get_task_queue(
    claims: IAccidentRepository = Depends(get_claims_repository),
) -> ITaskQueue:
    return TaskQueueFacade(claims)


def get_ais_gateway() -> IAisOsagoGateway:
    return AisOsagoFacade()


def build_accident_service(
    claims: IAccidentRepository = Depends(get_claims_repository),
    audit: AuditService = Depends(get_audit_service),
    strategy: Annotated[
        str,
        Query(description="Алгоритм назначения эксперта: free — первый свободный, region — по региону ДТП"),
    ] = "free",
) -> IAccidentService:
    """Динамический выбор стратегии назначения эксперта в рантайме."""
    assignment: AssignmentStrategy
    if strategy == "region":
        assignment = RegionExpertStrategy(claims)
    else:
        assignment = FreeExpertStrategy(claims)
    return AccidentService(claims, audit, assignment)


def build_inspection_service(
    claims: IAccidentRepository = Depends(get_claims_repository),
    files: IFileRepository = Depends(get_files_repository),
    audit: AuditService = Depends(get_audit_service),
    tasks: ITaskQueue = Depends(get_task_queue),
    ais: IAisOsagoGateway = Depends(get_ais_gateway),
) -> IInspectionService:
    return InspectionService(claims, files, audit, tasks, ais)
