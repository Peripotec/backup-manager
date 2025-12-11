from sqlmodel import Session, select, delete
from app.core.database import engine
from app.models.models import Device, Backup

def reset_db():
    print("WARNING: This will delete ALL devices and backups from the database.")
    confirm = input("Are you sure? (Type 'yes' to confirm): ")
    if confirm != "yes":
        print("Operation cancelled.")
        return

    with Session(engine) as session:
        # Delete backups first due to foreign key constraints
        print("Deleting backups...")
        session.exec(delete(Backup))
        
        print("Deleting devices...")
        session.exec(delete(Device))
        
        session.commit()
        print("Database cleared successfully.")

if __name__ == "__main__":
    reset_db()
