import time
from fastapi import Request
from app.core.config import get_settings
from app.core.errors import AppError
_MEMORY_BUCKET: dict[str, tuple[int, int]] = {}
def check_rate_limit(request: Request, api_key_id: str) -> None:
    settings=get_settings(); window=int(time.time())//settings.rate_limit_window_seconds
    key=f"{api_key_id}:{window}"; count,_=_MEMORY_BUCKET.get(key,(0,window)); count+=1; _MEMORY_BUCKET[key]=(count,window)
    if count > settings.rate_limit_requests:
        raise AppError("rate_limit_exceeded", "Too many requests.", 429)
