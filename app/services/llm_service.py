import requests

from app.core.config import settings


class LLMServiceError(Exception):
    pass


def call_groq(prompt: str) -> str:
    if not settings.groq_api_key:
        raise LLMServiceError("GROQ_API_KEY is not configured.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.groq_model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1200,
        "temperature": 0,
        "top_p": 1,
        "response_format": {"type": "json_object"},
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120,
        )
    except requests.RequestException as error:
        raise LLMServiceError(f"Could not reach Groq: {error}") from error

    if not response.ok:
        raise LLMServiceError(
            f"Groq error: {response.status_code} {response.text}"
        )

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as error:
        raise LLMServiceError(
            f"Unexpected Groq response: {response.text}"
        ) from error

    if isinstance(content, list):
        content = "".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        )

    if not isinstance(content, str) or not content.strip():
        raise LLMServiceError("Groq returned an empty response.")

    return content
