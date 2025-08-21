import pytest
from httpx import AsyncClient, ASGITransport
from main import app

# Test 1: Upload, Info, Delete
@pytest.mark.asyncio
async def test_file_upload_and_delete(tmp_path):
    test_file = tmp_path / "students.csv"
    test_file.write_text("name,age\nAman,21\nRiya,25")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        with open(test_file, "rb") as f:
            response = await client.post(
                "/files",
                files={"file": ("students.csv", f, "text/csv")}
            )
        assert response.status_code == 200
        file_id = response.json()["file_id"]

        resp_info = await client.get(f"/files/{file_id}")
        assert resp_info.status_code == 200
        assert "status" in resp_info.json()

        del_resp = await client.delete(f"/files/{file_id}")
        assert del_resp.status_code == 200
        assert del_resp.json()["detail"] == "File deleted successfully"

        final_check = await client.get(f"/files/{file_id}")
        assert final_check.status_code == 404



# Test 2: List All Files
@pytest.mark.asyncio
async def test_list_files(tmp_path):
    test_file = tmp_path / "data.csv"
    test_file.write_text("id,marks\n1,85\n2,90")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        with open(test_file, "rb") as f:
            response = await client.post(
                "/files",
                files={"file": ("data.csv", f, "text/csv")}
            )
        assert response.status_code == 200

        list_resp = await client.get("/files")
        assert list_resp.status_code == 200
        files = list_resp.json()

        assert isinstance(files, list)
        assert len(files) > 0
