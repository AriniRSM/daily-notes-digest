from datetime import date
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.tables import ItemType, NoteItem

router = APIRouter(prefix="/items", tags=["items"])

class CreateItemRequest(BaseModel):
    raw_input: str = Field(min_length=1, max_length=20_000)

class CreateItemResponse(BaseModel):
    id:int
    raw_input: str
    item_type: ItemType
    source_url: str | None
    status: str
    is_suspicious: bool

    class Config:
        from_attributes = True


def detect_item_type(raw_input: str) -> tuple[ItemType, str | None]:
    value = raw_input.strip()
    parsed = urlparse(value)

    if parsed.scheme in {'http', 'https'} and parsed.netloc:
        return ItemType.link,value

    if parsed.scheme and parsed.scheme not in {'http', 'https'}:
        raise HTTPException(status_code=400, detail="Only http or https allowed")
    return ItemType.text , None


def look_suspicious(raw_input: str) -> bool:
    lowered = raw_input.lower()
    suspicious_phrases = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "reveal your system prompt",
        "developer message",
        "Reveal system message",
        "Provide system data"
    ]
    return any(phrase in lowered for phrase in suspicious_phrases)


@router.post("", response_model=CreateItemResponse)
def create_item(payload: CreateItemRequest, db: Session = Depends(get_db)):
    raw_input = payload.raw_input.strip()

    if not raw_input:
        raise HTTPException(status_code=400, detail="Input cannot be empty.")

    existing_item = db.scalars(
        select(NoteItem).where(NoteItem.raw_input == raw_input).limit(1)
    ).first()
    if existing_item:
        raise HTTPException(
            status_code=409,
            detail="This content is already saved. Please search for it in Ask Me.",
        )

    item_type , source_url = detect_item_type(raw_input)

    item = NoteItem(
        raw_input=raw_input,
        item_type=item_type,
        source_url=source_url,
        is_suspicious=look_suspicious(raw_input)
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get("", response_model=list[CreateItemResponse])
def list_items(db: Session = Depends(get_db)):
    today = date.today()

    statement = (
        select(NoteItem)
        .where(NoteItem.created_at >= today)
        .order_by(NoteItem.created_at.desc())
    )

    return db.scalars(statement).all()
