import sys
import os
sys.path.append(os.getcwd())

from app.db.database import create_all_tables

def run_migrations():
    print("Starting database migrations...")
    try:
        create_all_tables()
        print("Database migrations completed successfully.")
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()
