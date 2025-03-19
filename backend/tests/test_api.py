import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# ✅ Test if the API is running
def test_home():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Scheduler API is running!"}

# ✅ Test fetching agents
def test_get_agents():
    response = requests.get(f"{BASE_URL}/api/agents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Agents should be a list

# ✅ Test fetching customers
def test_get_customers():
    response = requests.get(f"{BASE_URL}/api/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)  # Should return {"customers": [...]}

# ✅ Test starting simulation
def test_start_simulation():
    response = requests.post(f"{BASE_URL}/api/simulation/start")
    assert response.status_code == 200
    assert "Simulation started" in response.json()["message"]
