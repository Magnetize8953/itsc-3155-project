import pytest
from fastapi.testclient import TestClient
from api.main import app
client = TestClient(app)

from api.controllers.reviews import *
from api.dependencies.database import get_db

db = get_db()



def test_create():
    new_item = {"text": "Awful", "rating": 1, "customer_id": 16}
    item_response = {"text": "Awful", "rating": 1, "customer_id": 16, "id": 43}
    response = client.post("/reviews/", json=new_item)

    assert response.status_code == 200
    assert response.json() == item_response


def test_read_one():
    response = client.get("/reviews/43")
    assert response.status_code == 200
    assert response.json() == {"text": "Awful", "rating": 1, "customer_id": 16, "id": 43}

def test_update():
    request = {"text": "Great", "rating": 5}
    response = client.put("/reviews/43",json=request)
    print("Actual:")
    print(response.json())
    
    assert response.status_code == 200
    assert response.json() == {"text": "Great", "rating": 5, "customer_id": 16, "id": 43}

def test_read_not_found():
    response = client.get("/reviews/6")
    assert response.status_code == 404

def test_read_all():
    response = client.get("/reviews/")
    assert response.status_code == 200
    print("Actual:")
    print(response.json())
    assert response.json() == [{"text": "Great", "rating": 5, "customer_id": 16, "id": 43}]

def test_delete():
    response = client.delete("/reviews/43")
    assert response.status_code == 204

    

    
    
