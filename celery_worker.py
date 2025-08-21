import csv, io, json, os
from celery import Celery
from database import SessionLocal
from models import File

celery = Celery(__name__, broker=os.getenv("REDIS_URL", "redis://redis:6379/0"))

@celery.task
def parse_file(file_id: str):
    db = SessionLocal()
    file = db.query(File).filter(File.id == file_id).first()
    try:
        if not file:
            return

        file.status = "processing"
        file.progress = 0
        db.commit()

        with open(file.path, "rb") as f:
            content_bytes = f.read()

        reader = csv.DictReader(io.StringIO(content_bytes.decode()))
        rows = []
        for i, row in enumerate(reader, start=1):
            rows.append(row)
            if i % 50 == 0:   
                file.progress = min(90, file.progress + 10)
                db.commit()

        file.content = rows  
        file.status = "ready"
        file.progress = 100
        db.commit()

    except Exception as e:
        file.status = "error"
        file.progress = 100
        file.error = str(e)   
        db.commit()

    finally:
        db.close()
