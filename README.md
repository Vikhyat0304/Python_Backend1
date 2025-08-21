Python_Back/
│── main.py
│── test_main.py
│── requirements.txt
│── README.md
│── celery_worker.py
|── models.py
|── Dockerfile
|── docker-composer.yml

# File Manager API (FastAPI)

A simple FastAPI project for uploading, listing, retrieving, and deleting files.  
Includes tests and Postman collection.

---

## 🚀 Setup Instructions

```bash
# Clone repo
git clone https://github.com/your-username/python-back.git
cd python-back

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# Run tests
pytest -v

Server will run at:
👉 http://127.0.0.1:8000

📚 API Documentation

FastAPI provides auto docs:
Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc


🔗 Endpoints
1. Upload File

POST /files
Request (form-data):

{
  "file": "<your file>"
}

Response:

{
  "file_id": "43ad8d8a-7b30-45f6-b8e8-6964754624de",
  "status": "uploading"
}

2. List Files
GET /files

Response:

{
  "id": "43ad8d8a-7b30-45f6-b8e8-6964754624de",
  "filename": "resume.pdf",
  "status": "ready",
  "progress": 100,
  "content": "Parsing not supported for this file type",
  "path": "uploads/43ad8d8a-7b30-45f6-b8e8-6964754624de_resume.pdf",
  "created_at": "2025-08-21T00:46:17.951229"
}

3. Get File by ID
GET /files/{file_id}

Response:

{
  "file_id": "43ad8d8a-7b30-45f6-b8e8-6964754624de",
  "status": "ready",
  "progress": 100
}

4. Delete File
DELETE /files/{file_id}

Response:

{
  "detail": "File deleted successfully"
}

---

(USED BUT THROWING A LOT ERRORS JUST A DEMO OF HOW IT WILL WORK IF IMPLEMENTED)
## 📬 postman_collection.json
```json
{
  "info": {
    "name": "File Manager API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Upload File",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "file",
              "type": "file",
              "src": "data.csv"
            }
          ]
        },
        "url": {
          "raw": "http://127.0.0.1:8000/files",
          "protocol": "http",
          "host": ["127.0.0.1"],
          "port": "8000",
          "path": ["files"]
        }
      }
    },
    {
      "name": "List Files",
      "request": { "method": "GET", "url": "http://127.0.0.1:8000/files" }
    },
    {
      "name": "Get File",
      "request": { "method": "GET", "url": "http://127.0.0.1:8000/files/{{file_id}}" }
    },
    {
      "name": "Delete File",
      "request": { "method": "DELETE", "url": "http://127.0.0.1:8000/files/{{file_id}}" }
    }
  ]
}
