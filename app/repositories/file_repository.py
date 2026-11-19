from __future__ import annotations

from pathlib import Path
from uuid import UUID

from app.domain.entities import Photo, Signature
from app.repositories.interfaces import IFileRepository


class FileRepository(IFileRepository):
    """Файловое хранилище (демонстрационная замена MongoDB/GridFS)."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def save_photos(self, claim_id: UUID, photos: list[Photo]) -> list[UUID]:
        folder = self._claim_dir(claim_id) / "photos"
        folder.mkdir(parents=True, exist_ok=True)
        saved: list[UUID] = []
        for photo in photos:
            (folder / f"{photo.photo_id}.bin").write_bytes(photo.content)
            (folder / f"{photo.photo_id}.meta").write_text(photo.meta, encoding="utf-8")
            saved.append(photo.photo_id)
        return saved

    def get_photos(self, claim_id: UUID) -> list[Photo]:
        folder = self._claim_dir(claim_id) / "photos"
        if not folder.exists():
            return []
        photos: list[Photo] = []
        for meta_file in sorted(folder.glob("*.meta")):
            content_file = folder / f"{meta_file.stem}.bin"
            if not content_file.exists():
                continue
            photos.append(
                Photo(
                    content=content_file.read_bytes(),
                    meta=meta_file.read_text(encoding="utf-8"),
                    photo_id=UUID(meta_file.stem),
                )
            )
        return photos

    def save_signature(self, claim_id: UUID, signature: Signature) -> UUID:
        folder = self._claim_dir(claim_id)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "signature.bin").write_bytes(signature.content)
        (folder / "signature.meta").write_text(signature.signed_by, encoding="utf-8")
        return signature.signature_id

    def save_pdf(self, claim_id: UUID, content: bytes) -> UUID:
        folder = self._claim_dir(claim_id)
        folder.mkdir(parents=True, exist_ok=True)
        protocol_path = folder / "protocol.pdf"
        protocol_path.write_bytes(content)
        return claim_id

    def get_pdf(self, claim_id: UUID) -> bytes | None:
        protocol_path = self._claim_dir(claim_id) / "protocol.pdf"
        if not protocol_path.exists():
            return None
        return protocol_path.read_bytes()

    def _claim_dir(self, claim_id: UUID) -> Path:
        return self._root / str(claim_id)
