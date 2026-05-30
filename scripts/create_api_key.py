import sys
from app.db.database import SessionLocal
from app.services.api_key_service import ApiKeyService
if __name__=="__main__":
    name=sys.argv[1] if len(sys.argv)>1 else "Test Merchant"
    db=SessionLocal()
    try:
        row, generated=ApiKeyService(db).create(name)
        print("API key created.")
        print(f"ID: {row.id}")
        print(f"Prefix: {row.prefix}")
        print(f"Plain key: {generated.plain}")
    finally:
        db.close()
