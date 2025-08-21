from fastapi import FastAPI, UploadFile, File, HTTPException
import os, uuid, csv, asyncio
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

files_db = {}

@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    files_db[file_id] = {
        "id": file_id,
        "filename": file.filename,
        "status": "uploading",
        "progress": 0,
        "content": None,
        "path": file_path,
        "created_at": datetime.utcnow().isoformat()
    }
    asyncio.create_task(parse_file(file_id))
    return {"file_id": file_id, "status": "uploading"}


async def parse_file(file_id: str):
    file_info = files_db[file_id]
    file_info["status"] = "processing"
    for i in range(1, 6):
        await asyncio.sleep(1)  
        file_info["progress"] = i * 20
    try:
        if file_info["filename"].endswith(".csv"):
            with open(file_info["path"], newline="") as f:
                reader = csv.DictReader(f)
                file_info["content"] = [row for row in reader]
        elif file_info["filename"].endswith(".txt"):
            with open(file_info["path"], "r") as f:
                file_info["content"] = f.read()
        else:
            file_info["content"] = "Parsing not supported for this file type"

        file_info["status"] = "ready"
        file_info["progress"] = 100
    except Exception as e:
        file_info["status"] = "failed"


@app.get("/files/{file_id}")
async def get_file(file_id: str):
    file_info = files_db.get(file_id)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    if file_info["status"] != "ready":
        return {"message": "File upload or processing in progress. Please try again later."}

    return file_info

@app.get("/files")
async def list_files():
    return list(files_db.values())

@app.get("/files/{file_id}/progress")
async def file_progress(file_id: str):
    file_info = files_db.get(file_id)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    return {"file_id": file_id, "status": file_info["status"], "progress": file_info["progress"]}

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    file_info = files_db.get(file_id)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    if os.path.exists(file_info["path"]):
        os.remove(file_info["path"])

    del files_db[file_id]
    return {"detail": "File deleted successfully"}
