from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_requires_request_body():
    response = client.post("/api/auth/register")

    assert response.status_code == 400
    assert response.json()["detail"] == "Request body is required."


def test_register_missing_name():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "",
            "email": "missingname@finmark.local",
            "password": "SecurePass123",
            "role": "staff",
            "department": "operations"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Name is required."


def test_register_missing_email():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "",
            "password": "SecurePass123",
            "role": "staff",
            "department": "operations"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required."


def test_register_invalid_email_format():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "invalidemail",
            "password": "SecurePass123",
            "role": "staff",
            "department": "operations"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "A valid email address is required."


def test_register_short_password():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "shortpassword@finmark.local",
            "password": "123",
            "role": "staff",
            "department": "operations"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Password is too short. Minimum password length is 8 characters."


def test_register_success_with_valid_data():
    unique_email = f"validuser-{uuid4()}@finmark.local"

    response = client.post(
        "/api/auth/register",
        json={
            "name": "Valid User",
            "email": unique_email,
            "password": "SecurePass123",
            "role": "staff",
            "department": "operations"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
    assert response.json()["user"]["email"] == unique_email


def test_login_requires_request_body():
    response = client.post("/api/auth/login")

    assert response.status_code == 400
    assert response.json()["detail"] == "Request body is required."


def test_login_missing_email():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "",
            "password": "SecurePass123"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required."


def test_login_missing_password():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@finmark.local",
            "password": ""
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Password is required."


def test_login_invalid_user():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "notfound@finmark.local",
            "password": "wrongpass123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_dashboard_requires_token():
    response = client.get("/api/dashboard/summary")

    assert response.status_code == 401


def test_system_services_health():
    response = client.get("/api/system/services")

    assert response.status_code == 200
    assert response.json()["auth_service"] == "working"