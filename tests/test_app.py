from app import app

def test_home_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    # HTML page still contains this text
    assert b"Hello from Python CI/CD Project" in response.data
