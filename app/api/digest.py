from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.schema import DailyDigestOutput
from app.services.digest_service import (
    DigestGenerationError,
    NoItemsForDigestError,
    digest_row_to_output,
    generate_llm_digest_for_date,
    latest_digest,
)
from app.services.llm_service import LLMServiceError
from app.services.output_validators import OutputValidationError


router = APIRouter(prefix="/digest", tags=["digest"])


@router.post("/today", response_model=DailyDigestOutput)
def generate_today_digest(
    target_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        return generate_llm_digest_for_date(db, target_date or date.today())
    except NoItemsForDigestError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except LLMServiceError as error:
        raise HTTPException(
            status_code=502,
            detail=f"LLM provider failed: {error}",
        ) from error
    except OutputValidationError as error:
        raise HTTPException(
            status_code=422,
            detail=f"LLM output failed validation: {error}",
        ) from error
    except DigestGenerationError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Digest generation failed: {error}",
        ) from error


@router.get("/data", response_model=DailyDigestOutput)
def get_digest_data(db: Session = Depends(get_db)):
    digest = latest_digest(db)

    if not digest:
        raise HTTPException(status_code=404, detail="No digest has been generated yet.")

    return digest_row_to_output(digest)
