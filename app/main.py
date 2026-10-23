"""Точка сборки ИС ОСАГО: API (FastAPI) в части фиксации ДТП."""

from __future__ import annotations

import logging
import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.accident_controller import router as accident_router
from app.api.inspection_controller import router as inspection_router
from app.config import DB_PATH, STATIC_DIR, STORAGE_DIR
from app.domain.errors import DomainError, IntegrationError, NotFoundError
from app.repositories.accident_repository import AccidentRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        AccidentRepository(connection)
    finally:
        connection.close()
    yield


app = FastAPI(
    title="ИС ОСАГО — API фиксации ДТП",
    description="Лабораторная работа 3. Компонент API (FastAPI): заявления о ДТП, "
    "осмотр, подпись клиента, генерация PDF-протокола.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(IntegrationError)
async def integration_handler(request: Request, exc: IntegrationError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


app.include_router(accident_router)
app.include_router(inspection_router)
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
