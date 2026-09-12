"""
HealthAware AI - Multi-Format Document Ingestion Pipeline
Extracts text from PDF, DOCX, TXT, JSON, and CSV documents,
chunks the content, generates embeddings, and saves into the vector knowledge store.
"""

import os
import json
import csv
import io
from pathlib import Path
from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session

import pypdf
import docx

from rag.chunking import chunk_text
from rag.embeddings import get_embedding_provider
from database.repositories import DocumentRepository


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract clean text content from various file formats."""
    ext = Path(filename).suffix.lower()

    if ext in [".txt", ".tsv"]:
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = file_bytes.decode("latin-1")
        if ext == ".tsv":
            # Keep tabular disease references readable and searchable.
            lines = text.splitlines()
            if lines and len(lines[0].split("\t")) > 1:
                return "\n".join(
                    " | ".join(line.split("\t")) for line in lines if line.strip()
                )
        return text

    elif ext == ".pdf":
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages_text.append(text)
        return "\n\n".join(pages_text)

    elif ext in [".docx", ".doc"]:
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)

    elif ext == ".json":
        data = json.loads(file_bytes.decode("utf-8"))
        if isinstance(data, list):
            # List of items or QA pairs
            parts = []
            for item in data:
                if isinstance(item, dict):
                    parts.append("\n".join(f"{k}: {v}" for k, v in item.items()))
                else:
                    parts.append(str(item))
            return "\n\n".join(parts)
        elif isinstance(data, dict):
            return "\n".join(f"{k}: {v}" for k, v in data.items())
        return str(data)

    elif ext == ".csv":
        content = file_bytes.decode("utf-8", errors="ignore")
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        if not rows:
            return ""
        header = rows[0]
        text_lines = []
        for row in rows[1:]:
            line = ", ".join(f"{header[i]}: {row[i]}" for i in range(min(len(header), len(row))))
            text_lines.append(line)
        return "\n".join(text_lines)

    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats are PDF, DOCX, TXT, JSON, CSV.")


def ingest_document(
    db: Session,
    filename: str,
    file_bytes: bytes,
    title: str = "",
    category: str = "General Health",
    source_citation: str = ""
) -> Tuple[bool, str, int]:
    """
    Complete ingestion pipeline:
    1. Extract text
    2. Clean & chunk
    3. Generate embeddings
    4. Store in database
    """
    try:
        text = extract_text_from_file(file_bytes, filename)
        if not text.strip():
            return False, "File is empty or no readable text could be extracted.", 0

        ext = Path(filename).suffix.lower().replace(".", "")
        doc_title = title.strip() or Path(filename).stem.replace("_", " ").title()
        citation = source_citation.strip() or f"HealthAware Knowledge Base: {doc_title}"

        # 1. Register Document
        doc = DocumentRepository.add_document(
            db=db,
            filename=filename,
            file_type=ext,
            title=doc_title,
            category=category,
            source_citation=citation
        )

        # 2. Chunk text
        metadata = {
            "title": doc_title,
            "category": category,
            "source": citation,
            "filename": filename
        }
        raw_chunks = chunk_text(text, chunk_size=300, overlap=40, metadata=metadata)

        # 3. Generate embeddings
        provider = get_embedding_provider()
        processed_chunks = []
        for c in raw_chunks:
            emb = provider.embed_text(c["content"])
            processed_chunks.append({
                "chunk_index": c["chunk_index"],
                "content": c["content"],
                "metadata": c["metadata"],
                "embedding": emb
            })

        # 4. Save chunks
        chunks_count = DocumentRepository.add_chunks(db, doc.id, processed_chunks)
        return True, f"Successfully ingested {filename} ({chunks_count} chunks indexed).", chunks_count

    except Exception as e:
        return False, f"Failed to ingest {filename}: {str(e)}", 0
