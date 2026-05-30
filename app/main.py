from fastapi import FastAPI
from app.api.routes.api_keys import router as api_keys_router
from app.api.routes.health import router as health_router
from app.api.routes.payments import router as payments_router
from app.api.routes.processors import router as processors_router
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.middleware.request_id import RequestIdMiddleware

def create_app() -> FastAPI:
    configure_logging()
    app=FastAPI(title="RightWare Payment Gateway", version="0.2.0")
    app.add_middleware(RequestIdMiddleware)
    register_error_handlers(app)
    app.include_router(health_router)
    app.include_router(api_keys_router)
    app.include_router(payments_router)
    app.include_router(processors_router)
    return app
app=create_app()
