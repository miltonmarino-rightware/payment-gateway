import logging, sys, structlog
from app.core.config import get_settings

def mask_sensitive_data(logger, method_name, event_dict):
    """
    Mask sensitive data like card numbers, cvc, etc. in logs.
    """
    sensitive_keys = ["card_number", "cvc", "cvv", "api_key", "password"]
    for key in sensitive_keys:
        if key in event_dict:
            event_dict[key] = "********"
    return event_dict

def configure_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        format="%(message)s", 
        stream=sys.stdout, 
        level=getattr(logging, settings.log_level.upper(), logging.INFO)
    )
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            mask_sensitive_data,
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True
    )
