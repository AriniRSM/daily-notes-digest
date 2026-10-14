import json

from pydantic import ValidationError

from app.models.schema import DailyDigestOutput


class OutputValidationError(Exception):
    pass


def extract_json_object(raw_text: str) -> dict:
    start = raw_text.find("{")
    end = raw_text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise OutputValidationError("LLM output did not contain a JSON object.")

    json_text = raw_text[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as error:
        raise OutputValidationError(f"Invalid JSON from LLM: {error}") from error


def validate_digest_output(raw_text: str) -> DailyDigestOutput:
    data = extract_json_object(raw_text)

    try:
        return DailyDigestOutput.model_validate(data)
    except ValidationError as error:
        raise OutputValidationError(str(error)) from error