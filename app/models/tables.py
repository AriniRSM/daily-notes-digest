from datetime import datetime
from enum import Enum

from pydantic.v1 import HttpUrl
from sqlalchemy import Boolean, DateTime, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, JSON

from app.core.db import Base

class ItemType(str, Enum):
    link = "link"
    text = "text"

class ItemStatus(str, Enum):
    saved = "saved"
    processing = "processing"
    processed = "processed"
    failed = "failed"

class NoteItem(Base):
    __tablename__ = "note_items"

    id: Mapped[int] = mapped_column(primary_key=True, index= True)
    raw_input: Mapped[str] = mapped_column(Text, nullable = False)
    item_type: Mapped[ItemType] = mapped_column(SqlEnum(ItemType), nullable = False)
    source_url: Mapped[HttpUrl | None] = mapped_column(Text, nullable = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[ItemStatus] = mapped_column(SqlEnum(ItemStatus),default=ItemStatus.saved, nullable = False)
    is_suspicious: Mapped[bool] = mapped_column(Boolean, default=False)
    fetch_error: Mapped[str | None] = mapped_column(Text, nullable = True)

class ProcessedContent(Base):
    __tablename__ = "processed_content"

    id: Mapped[int] = mapped_column(primary_key=True, index = True)
    note_item_id: Mapped[int] = mapped_column(ForeignKey("note_items.id"), nullable = False)

    title: Mapped[str] = mapped_column(Text, nullable = True)
    extracted_text: Mapped[str] = mapped_column(Text, nullable = True)
    summary: Mapped[str] = mapped_column(Text, nullable = True)
    content_preview: Mapped[str | None] = mapped_column(Text, nullable = True)

    risk_flags: Mapped[list] = mapped_column(JSON, nullable = True)
    processed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class DailyDigest(Base):
    __tablename__ = "daily_digest"

    id: Mapped[int] = mapped_column(primary_key=True, index = True)
    digest_date: Mapped[DateTime] = mapped_column(DateTime, nullable = False)

    title: Mapped[str] = mapped_column(Text, nullable = False)
    overview_topics: Mapped[list] = mapped_column(JSON, default= list)
    summaries: Mapped[list] = mapped_column(JSON, default= list)
    links: Mapped[list] = mapped_column(JSON, default= list)
    action_items: Mapped[list] = mapped_column(JSON, default= list)

    output_validation_status: Mapped[str] = mapped_column(Text, default="valid")
    output_validation_errors: Mapped[list] = mapped_column(JSON, default= list)

    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
