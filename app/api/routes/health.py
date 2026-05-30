from fastapi import APIRouter
from sqlalchemy import text
from app.core.config import get_settings
from app.db.database import engine
router=APIRouter(tags=["system"])
@router.get("/health")
def health_check():
    database="ok"
    try:
        with engine.connect() as conn: conn.execute(text("select 1"))
    except Exception: database="error"
    return {"status":"healthy" if database=="ok" else "degraded","database":database,"redis":"not_required_mvp","version":get_settings().app_version}
