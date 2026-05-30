import hashlib, hmac, secrets
from dataclasses import dataclass
from app.core.config import get_settings

@dataclass(frozen=True)
class GeneratedApiKey:
    plain: str
    prefix: str
    key_hash: str

def hash_secret(value: str, pepper: str | None = None) -> str:
    secret_pepper = pepper or get_settings().api_key_pepper
    return hashlib.sha256(f"{value}:{secret_pepper}".encode()).hexdigest()

def constant_time_equals(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)

def generate_api_key(prefix: str = "rw_test") -> GeneratedApiKey:
    plain = f"{prefix}_{secrets.token_urlsafe(32)}"
    return GeneratedApiKey(plain=plain, prefix=plain[:12], key_hash=hash_secret(plain))
