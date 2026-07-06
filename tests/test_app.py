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

def test_service_catalog_available():
    response = client.get("/api/services/catalog")

    assert response.status_code == 200
    assert response.json()["message"] == "FinMark service catalog retrieved successfully"
    assert len(response.json()["services"]) >= 4


def test_place_order_requires_request_body():
    response = client.post("/api/orders/place")

    assert response.status_code == 400
    assert response.json()["detail"] == "Request body is required."


def test_place_order_missing_customer_name():
    response = client.post(
        "/api/orders/place",
        json={
            "customer_name": "",
            "customer_email": "client@finmark.local",
            "client_type": "retail",
            "service_id": 1,
            "order_notes": "Need financial analysis."
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Customer name is required."


def test_place_order_invalid_customer_email():
    response = client.post(
        "/api/orders/place",
        json={
            "customer_name": "ABC Retail Group",
            "customer_email": "invalidemail",
            "client_type": "retail",
            "service_id": 1,
            "order_notes": "Need financial analysis."
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "A valid customer email address is required."


def test_place_order_success():
    response = client.post(
        "/api/orders/place",
        json={
            "customer_name": "Milestone Test Client",
            "customer_email": "milestoneclient@finmark.local",
            "client_type": "e-commerce",
            "service_id": 1,
            "order_notes": "Need financial analysis for projected growth."
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Service order placed successfully"
    assert response.json()["order"]["customer_email"] == "milestoneclient@finmark.local"
    assert response.json()["order"]["order_status"] == "pending"
    assert response.json()["order"]["payment_status"] == "pending"


def test_orders_list_available():
    response = client.get("/api/orders/list")

    assert response.status_code == 200
    assert response.json()["message"] == "Service orders retrieved successfully"


def test_events_available():
    response = client.get("/api/events")

    assert response.status_code == 200
    assert response.json()["message"] == "Event bus records retrieved successfully"


def test_audit_logs_available():
    response = client.get("/api/audit-logs")

    assert response.status_code == 200
    assert response.json()["message"] == "Audit logs retrieved successfully"

def test_customer_registration_success():
    unique_email = f"customer-{uuid4()}@finmark.local"

    response = client.post(
        "/api/auth/register",
        json={
            "name": "Customer Test User",
            "email": unique_email,
            "password": "SecurePass123",
            "role": "customer",
            "department": "client"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
    assert response.json()["user"]["role"] == "customer"
    assert response.json()["user"]["department"] == "client"


def test_customer_login_returns_customer_role():
    unique_email = f"customer-login-{uuid4()}@finmark.local"

    register_response = client.post(
        "/api/auth/register",
        json={
            "name": "Customer Login User",
            "email": unique_email,
            "password": "SecurePass123",
            "role": "customer",
            "department": "client"
        }
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": unique_email,
            "password": "SecurePass123"
        }
    )

    assert login_response.status_code == 200
    assert login_response.json()["user"]["role"] == "customer"


def test_customer_cannot_access_dashboard_summary():
    unique_email = f"customer-dashboard-{uuid4()}@finmark.local"

    register_response = client.post(
        "/api/auth/register",
        json={
            "name": "Customer Dashboard User",
            "email": unique_email,
            "password": "SecurePass123",
            "role": "customer",
            "department": "client"
        }
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": unique_email,
            "password": "SecurePass123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["token"]

    dashboard_response = client.get(
        "/api/dashboard/summary",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert dashboard_response.status_code == 403
    assert dashboard_response.json()["detail"] == "Customers can place service orders but cannot access the employee dashboard."

def test_system_health_available():
    response = client.get("/api/system/health")

    assert response.status_code == 200
    assert "overall_status" in response.json()
    assert "database" in response.json()
    assert "services" in response.json()
    assert "rate_limiting" in response.json()


def test_system_resilience_available():
    response = client.get("/api/system/resilience")

    assert response.status_code == 200
    assert response.json()["message"] == "FinMark prototype resilience features are enabled."
    assert "rate_limiting" in response.json()["features"]
    assert "fallback_responses" in response.json()["features"]
    assert "audit_logging" in response.json()["features"]


def test_api_gateway_headers_present():
    response = client.get("/api/system/services")

    assert response.status_code == 200
    assert "X-Process-Time-ms" in response.headers
    assert response.headers["X-Prototype-Gateway"] == "FinMark API Gateway Middleware"