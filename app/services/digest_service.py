from datetime import date, datetime, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.schema import (
    DailyDigestOutput,
    DigestInputPayload,
    DigestLink,
    DigestSummary,
)
from app.models.tables import DailyDigest, ItemType, NoteItem
from app.services.digest_prompt import build_digest_prompt
from app.services.llm_service import call_groq
from app.services.output_validators import OutputValidationError, validate_digest_output


class NoItemsForDigestError(Exception):
    pass


class DigestGenerationError(Exception):
    pass


def get_date_bounds(target_date: date) -> tuple[datetime, datetime]:
    return (
        datetime.combine(target_date, time.min),
        datetime.combine(target_date, time.max),
    )


def load_items_for_date(db: Session, target_date: date) -> list[NoteItem]:
    start, end = get_date_bounds(target_date)

    statement = (
        select(NoteItem)
        .where(NoteItem.created_at >= start)
        .where(NoteItem.created_at <= end)
        .order_by(NoteItem.created_at.asc())
    )

    return list(db.scalars(statement).all())


def make_preview(raw_input: str, limit: int = 250) -> str:
    value = raw_input.strip()
    if len(value) <= limit:
        return value
    return value[:limit] + "..."


def build_input_payload(items: list[NoteItem], target_date: date) -> DigestInputPayload:
    return DigestInputPayload(
        digest_date=target_date,
        items=[
            {
                "note_item_id": item.id,
                "raw_input": item.raw_input,
                "item_type": item.item_type.value,
                "source_url": item.source_url,
                "captured_at": item.created_at,
            }
            for item in items
        ],
    )


def normalize_url(value: object) -> str:
    return str(value).rstrip("/")


def validate_digest_against_input(
    digest_output: DailyDigestOutput,
    input_payload: DigestInputPayload,
) -> None:
    valid_note_ids = {item.note_item_id for item in input_payload.items}
    valid_link_urls = {
        normalize_url(item.source_url)
        for item in input_payload.items
        if item.item_type == ItemType.link.value and item.source_url
    }

    invalid_summary_ids = [
        summary.note_item_id
        for summary in digest_output.summaries
        if summary.note_item_id not in valid_note_ids
    ]

    if invalid_summary_ids:
        raise OutputValidationError(
            f"Digest contains unknown note_item_id values: {invalid_summary_ids}"
        )

    invented_links = [
        str(link.source_url)
        for link in digest_output.links
        if normalize_url(link.source_url) not in valid_link_urls
    ]

    if invented_links:
        raise OutputValidationError(f"Digest contains invented links: {invented_links}")


def save_digest(
    db: Session,
    digest_output: DailyDigestOutput,
    validation_status: str = "valid",
    validation_errors: list[str] | None = None,
) -> DailyDigestOutput:
    digest_row = DailyDigest(
        digest_date=datetime.combine(digest_output.digest_date, time.min),
        title=digest_output.title,
        overview_topics=digest_output.overview_topics,
        summaries=[
            summary.model_dump(mode="json")
            for summary in digest_output.summaries
        ],
        links=[
            link.model_dump(mode="json")
            for link in digest_output.links
        ],
        action_items=digest_output.action_items,
        output_validation_status=validation_status,
        output_validation_errors=validation_errors or [],
    )

    db.add(digest_row)
    db.commit()

    return digest_output


def generate_manual_digest_for_date(db: Session, target_date: date) -> DailyDigestOutput:
    items = load_items_for_date(db, target_date)

    if not items:
        raise NoItemsForDigestError("No items saved for this date.")

    summaries = []
    links = []

    for item in items:
        title = "Saved Link" if item.item_type == ItemType.link else "Saved Note"

        summaries.append(
            DigestSummary(
                note_item_id=item.id,
                title=title,
                item_type=item.item_type.value,
                source_url=item.source_url,
                captured_at=item.created_at,
                summary=make_preview(item.raw_input),
                content_preview=make_preview(item.raw_input, limit=120),
            )
        )

        if item.item_type == ItemType.link and item.source_url:
            links.append(
                DigestLink(
                    title=item.source_url,
                    source_url=item.source_url,
                )
            )

    digest_output = DailyDigestOutput(
        title=f"Daily Digest - {target_date.isoformat()}",
        overview_topics=["Captured notes"],
        digest_date=target_date,
        summaries=summaries,
        links=links,
        action_items=[],
    )

    return save_digest(db, digest_output, validation_status="manual", validation_errors=[])


def generate_llm_digest_for_date(db: Session, target_date: date) -> DailyDigestOutput:
    items = load_items_for_date(db, target_date)

    if not items:
        raise NoItemsForDigestError("No items saved for this date.")

    input_payload = build_input_payload(items, target_date)
    items_payload = [
        item.model_dump(mode="json")
        for item in input_payload.items
    ]

    prompt = build_digest_prompt(
        items_payload=items_payload,
        digest_date=input_payload.digest_date.isoformat(),
    )

    raw_output = call_groq(prompt)
    digest_output = validate_digest_output(raw_output)
    validate_digest_against_input(digest_output, input_payload)

    return save_digest(db, digest_output, validation_status="valid", validation_errors=[])


def latest_digest(db: Session) -> DailyDigest | None:
    statement = select(DailyDigest).order_by(DailyDigest.generated_at.desc())
    return db.scalars(statement).first()


def digest_row_to_output(row: DailyDigest) -> DailyDigestOutput:
    return DailyDigestOutput(
        title=row.title,
        overview_topics=row.overview_topics or [],
        digest_date=row.digest_date.date(),
        summaries=row.summaries or [],
        links=row.links or [],
        action_items=row.action_items or [],
    )
