from datetime import date, datetime, time
from pydantic import BaseModel, Field, HttpUrl

class DigestSummary(BaseModel):
    note_item_id: int
    title: str = Field(min_length=1, max_length=250)
    item_type: str
    source_url: HttpUrl | None = None
    captured_at: datetime | None = None
    summary: str = Field(min_length=1)
    content_preview: str | None = None

class DigestLink(BaseModel):
    title: str
    source_url: HttpUrl

class DailyDigestOutput(BaseModel):
    title: str = Field(min_length=1)
    overview_topics: list[str] = Field(default_factory=list , max_length=10)
    digest_date: date
    summaries: list[DigestSummary] = Field(default_factory=list)
    links: list[DigestLink] = Field(default_factory=list)
    action_items: list[str] = Field(default_factory=list, max_length=10)


class DigestInputItem(BaseModel):
    note_item_id: int
    raw_input: str = Field(min_length=1, max_length=20_000)
    item_type: str
    source_url: str | None = None
    captured_at: datetime | None = None


class DigestInputPayload(BaseModel):
    digest_date: date
    items: list[DigestInputItem] = Field(min_length=1)
