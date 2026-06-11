from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from loguru import logger
from app.core.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_SIZE_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024


async def save_upload(file: UploadFile, user_id: str) -> Tuple[str, str]:
    upload_dir = Path(settings.UPLOAD_DIR) / user_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type {ext} not supported. Use PDF, DOCX, or TXT.")

    content = await file.read()
    if len(content) > MAX_SIZE_BYTES:
        raise HTTPException(400, f"File too large. Max {settings.MAX_FILE_SIZE_MB}MB.")

    safe_name = f"{user_id[:8]}_{file.filename.replace(' ', '_')}"
    file_path = upload_dir / safe_name

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path), file.filename


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    try:
        if ext == ".pdf":
            return _extract_pdf(file_path)
        elif ext == ".docx":
            return _extract_docx(file_path)
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            raise HTTPException(400, f"Cannot extract text from {ext}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text extraction failed for {file_path}: {e}")
        raise HTTPException(500, f"Failed to extract text from file: {str(e)}")


def _extract_pdf(file_path: str) -> str:
    text_parts = []

    # Try pdfplumber first (best for text-based PDFs)
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        text = "\n".join(text_parts)
        if text.strip():
            return text
    except Exception as e:
        logger.warning(f"pdfplumber failed: {e}")

    # Fallback to PyMuPDF
    try:
        import fitz
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        if text.strip():
            return text
    except Exception as e:
        logger.warning(f"PyMuPDF failed: {e}")

    # If both fail, raise a clear error
    raise Exception(
        "Could not extract text from PDF. The file may be a scanned image. "
        "Please use a text-based PDF or convert it first."
    )


def _extract_docx(file_path: str) -> str:
    from docx import Document
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)
