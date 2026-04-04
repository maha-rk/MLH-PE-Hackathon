import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app import create_app

def test_health_endpoint():
    app = create_app()
    test_client = app.test_client()

    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


