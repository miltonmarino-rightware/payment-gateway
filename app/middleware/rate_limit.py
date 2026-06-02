import time
from fastapi import Request
from app.core.config import get_settings
from app.core.errors import AppError

# In-memory fallback when Redis is unavailable
_MEMORY_BUCKET: dict[str, tuple[int, int]] = {}

def check_rate_limit(request: Request, api_key_id: str) -> None:
    """
    Check rate limits per API key. Uses Redis if available, otherwise falls back to in-memory.
    """
    settings = get_settings()
    window = int(time.time()) // settings.rate_limit_window_seconds
    key = f"{api_key_id}:{window}"
    
    try:
        # Try Redis-based rate limiting
        import redis
        r = redis.from_url(settings.redis_url, decode_responses=True)
        count = r.incr(key)
        if count == 1:
            r.expire(key, settings.rate_limit_window_seconds)
        if count > settings.rate_limit_requests:
            raise AppError("rate_limit_exceeded", "Too many requests.", 429)
    except Exception:
        # Fallback to in-memory (for local dev or Redis unavailability)
        count, _ = _MEMORY_BUCKET.get(key, (0, window))
        count += 1
        _MEMORY_BUCKET[key] = (count, window)
        if count > settings.rate_limit_requests:
            raise AppError("rate_limit_exceeded", "Too many requests.", 429)
