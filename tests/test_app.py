from app import app


def test_home_page_loads():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"LogSentry" in response.data
    assert b"Upload" in response.data
