from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from config import settings

api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key: str = Security(api_key_header)):
    """Basic API key verification. Look into replacement after further development."""

    if api_key == settings.api_key:
        return api_key
    raise HTTPException(status_code=401, detail="Missing or invalid API key")