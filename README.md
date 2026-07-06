# **FinMark Milestone 2: Prototype**

## Project Overview

FinMark is a software development prototype based on the proposed system architecture for a secure, scalable, and resilient business service platform. The project is designed for FinMark Corporation, a company that provides financial analysis, marketing analytics, business intelligence, and consulting services to businesses in retail, e-commerce, healthcare, and manufacturing.

For Milestone 2, the prototype was refined from a basic login and dashboard system into a working application prototype with role-based access, customer service order placement, database-backed services, audit logging, event bus simulation, health monitoring, and basic resilience features.

The prototype demonstrates how FinMark can support both customer-facing service orders and employee-facing operations monitoring.

---

## Problem Statement

FinMark Corporation has recently gained several new customers, each with multiple users. The current system was originally designed for smaller-scale usage, but customer growth has increased the number of online service orders and system transactions.

The company currently supports around 500 online orders per day, but demand is projected to rise to 3,000 orders per day. Because of this growth, the system must become more reliable, scalable, and resilient. Customers have also started raising support tickets due to crashes and order processing issues.

The Software Development task is to improve the application so that it can handle missing or invalid user input, avoid crashes, and keep important operations running smoothly.

---

## Purpose of the Prototype

The purpose of this prototype is to create a working local version of the proposed FinMark platform. It demonstrates how customers can register, log in, and place service orders, while employees can monitor orders, payments, reports, audit logs, event bus records, and service health.

The prototype also demonstrates how missing or invalid data is handled with clear error messages instead of allowing the system to crash.

---

## Tools and Technologies Used

- Python
- FastAPI
- SQLite
- HTML
- CSS
- Bootstrap
- JavaScript
- VS Code
- GitHub
- Postman
- Pytest

---

## Main Features Implemented

The refined prototype includes the following working features:

- User registration
- User login
- Password hashing
- JWT token generation
- Role-based access control
- Customer role flow
- Employee dashboard access
- Customer service order placement
- Database-backed service catalog
- Database-backed service orders
- Database-backed payment records
- Database-backed dashboard metrics
- Reports page
- Monitoring page
- Audit log storage
- Event bus simulation
- API Gateway-style request timing
- Basic in-memory rate limiting
- System health check endpoint
- System resilience endpoint
- Automated Pytest tests

---

## User Roles

The system supports the following roles:

- Customer
- COO
- Admin
- Finance
- Operations
- Staff

Customer users are redirected to the service order page after login. Employee users such as COO, admin, finance, operations, and staff are redirected to the dashboard.

Customers can place service orders, but they are blocked from accessing the protected employee dashboard API.

---

## Customer Flow

The customer flow works as follows:

1. Customer registers an account.
2. Customer logs in using email and password.
3. The system creates a JWT token.
4. The customer is redirected to the service order page.
5. Customer name and email are automatically filled in.
6. Customer selects a client type and FinMark service.
7. Customer submits the service order.
8. The system saves the order in the database.
9. The system creates a payment record.
10. The system records an event bus entry.
11. The system records an audit log entry.
12. Employee dashboard and reports update based on the new order data.

---

## Employee Flow

The employee flow works as follows:

1. Employee registers or logs in.
2. The system validates the email and password.
3. The system creates a JWT token.
4. The employee is redirected to the dashboard.
5. The dashboard loads protected database-backed data.
6. Employee can view:
   - Dashboard
   - Orders
   - Services
   - Payments
   - Reports
   - Monitoring

---

## Frontend Implementation

The frontend includes the following pages:

- Login page
- Register page
- Customer service order page
- Dashboard page
- Orders page
- Services page
- Payments page
- Reports page
- Monitoring page

The frontend uses HTML, CSS, Bootstrap, and JavaScript. JavaScript connects the pages to the FastAPI backend through API requests. The JWT token is stored in browser localStorage after login and is used to access protected routes.

---

## Backend and API Implementation

The backend was built using FastAPI. The backend handles:

- Request validation
- User registration
- User login
- Password hashing
- JWT token generation
- Protected dashboard access
- Customer service order processing
- Payment record creation
- Audit logging
- Event bus recording
- System health checking
- Resilience status reporting
- API Gateway-style middleware

The frontend does not directly access the database. It sends requests to the backend API, and the backend handles validation, database operations, and responses.

---

## Database Implementation

SQLite is used as the local prototype database. The database contains multiple tables to simulate the proposed database layer.

Implemented tables:

- users
- service_catalog
- service_orders
- payments
- audit_logs
- event_bus

These tables represent a local prototype version of:

- Auth DB
- Product/Service Catalog DB
- Order DB
- Payment DB
- Audit Log Storage
- Async Message Bus

Passwords are stored as hashed values instead of plain text.

---

## FinMark Services

The service catalog contains the following FinMark services:

- Financial Analysis
- Marketing Analytics
- Business Intelligence
- Consulting Services

Because FinMark is a business service company, the Product Service is represented in this prototype as a Service Catalog.

---

## Input Validation and Error Handling

The prototype was improved to handle missing, null, or invalid inputs.

Validation was added for:

- Missing name
- Missing email
- Invalid email format
- Missing password
- Password shorter than 8 characters
- Missing role
- Invalid role
- Missing department
- Missing customer name
- Missing customer email
- Invalid customer email
- Missing client type
- Missing service selection
- Invalid login credentials
- Missing or invalid JWT token
- Customer attempting to access employee dashboard API

Instead of crashing, the system returns clear error messages.

---

## Resilience Features

The refined prototype includes basic resilience and reliability features.

Implemented resilience features:

- Input validation for missing and invalid data
- API Gateway-style middleware
- Request processing time logging
- Response headers for request timing
- Basic in-memory rate limiting
- Dashboard fallback responses
- System health check endpoint
- System resilience endpoint
- Audit logs for important actions
- Event bus records for service communication

These features help show how the application can remain stable when users submit incomplete data or when system monitoring is needed.

---

## API Gateway Simulation

The FastAPI middleware simulates part of the API Gateway layer.

It provides:

- API request timing
- Gateway response headers
- Basic rate limiting
- Logging of request performance

The rate limiting is a simple in-memory prototype version. In a production setup, this can be replaced with a more advanced API Gateway or Redis-backed rate limiter.

---

## Audit Logging

The system records important activities in the audit_logs table.

Examples of logged actions:

- user_registered
- register_validation_failed
- login_success
- login_failed
- dashboard_accessed
- dashboard_accessed_cache_hit
- service_order_created
- service_order_validation_failed

This improves traceability and supports system monitoring.

---

## Event Bus Simulation

The system uses an event_bus table to simulate asynchronous service communication.

Examples of event records:

- service_order_created
- payment_record_created

This represents a simplified local version of an Async Message Bus from the proposed architecture.

---

## Dashboard and Reporting

The dashboard now uses database-backed data instead of static sample values.

The dashboard shows:

- Projected revenue
- Estimated expenses
- Estimated net profit
- Payment records
- Available services
- Pending payments
- Order status
- Service health

The Reports page also summarizes:

- Total revenue
- Net profit
- Service orders
- Payment records
- Available services
- Pending revenue

---

## Alignment with Proposed System Architecture

The current prototype is aligned with the proposed architecture in a simplified local version.

Implemented or simulated components:

- Web Application: Login, Register, Dashboard, Orders, Services, Payments, Reports, Monitoring, and Customer Order pages
- API Gateway Layer: FastAPI routes and middleware
- JWT Validation and RBAC: JWT authentication and role-based access control
- Request Logging: API response time logging and headers
- Auth Service: Registration, login, password hashing, and JWT token generation
- Order Service: Database-backed customer service order processing
- Product Service: Database-backed FinMark service catalog
- Payment Service: Database-backed simulated payment records
- Financial Service: Database-backed financial summary calculations
- Auth DB: SQLite users table
- Order DB: SQLite service_orders table
- Product DB: SQLite service_catalog table
- Payment DB: SQLite payments table
- Audit Log Storage: SQLite audit_logs table
- Async Message Bus: SQLite event_bus table
- Cache: Simple in-memory dashboard cache
- Monitoring: Monitoring page, audit logs, event bus records, and health check endpoint
- Resilience: Input validation, fallback responses, and rate limiting simulation

---

## API Endpoints

Important API endpoints include:

- POST /api/auth/register
- POST /api/auth/login
- GET /api/dashboard/summary
- GET /api/services/catalog
- POST /api/orders/place
- GET /api/orders/list
- GET /api/orders/summary
- GET /api/payments/summary
- GET /api/products/summary
- GET /api/financials/summary
- GET /api/audit-logs
- GET /api/events
- GET /api/system/services
- GET /api/system/health
- GET /api/system/resilience

---

## Testing

The prototype was tested using browser testing, Postman API testing, and Pytest automated testing.

Browser testing included:

- Registering users
- Logging in as customer
- Logging in as employee
- Submitting customer service orders
- Viewing the dashboard
- Viewing orders
- Viewing services
- Viewing payments
- Viewing reports
- Viewing monitoring logs

Postman testing included:

- Register validation error
- Customer registration
- Customer login token
- Customer blocked from dashboard API
- Service order placement
- Orders list
- Employee login token
- Protected dashboard API
- System health API
- System resilience API
- Audit logs
- Event bus records

Pytest testing includes automated checks for:

- Health check
- Register validation
- Login validation
- Protected dashboard access
- Service catalog
- Order placement
- Orders list
- Audit logs
- Event bus
- Customer role registration
- Customer role login
- Customer blocked from dashboard
- System health
- System resilience
- API Gateway headers

Current automated test result:

- 27 passed
- 1 warning

The warning comes from FastAPI/TestClient dependency behavior and does not break the prototype.

---

## Challenges Encountered

Several challenges were encountered during development.

These included:

- Setting up the project folder structure
- Connecting frontend pages to backend APIs
- Handling JWT authentication
- Saving and checking records in SQLite
- Fixing FastAPI template rendering
- Updating Git and syncing groupmate commits
- Preventing Python cache files from being committed
- Handling incomplete user inputs
- Converting static placeholder services into database-backed services
- Creating a customer role flow separate from employee users
- Connecting order placement to payments, audit logs, event bus records, and dashboard updates

---

## What Worked

The following parts are working:

- User registration
- User login
- Password hashing
- JWT token generation
- Role-based routing
- Customer order page
- Employee dashboard page
- Customer service order placement
- Database-backed order records
- Database-backed payment records
- Database-backed service catalog
- Database-backed financial summaries
- Dashboard data loading
- Orders page
- Services page
- Payments page
- Reports page
- Monitoring page
- Audit logs
- Event bus simulation
- System health endpoint
- System resilience endpoint
- Basic rate limiting middleware
- Pytest automated testing

---

## Current Limitations

This is still a local prototype. Some production-level architecture components are simulated instead of fully deployed.

Current limitations:

- SQLite is used instead of separate production databases.
- The payment process is simulated.
- The event bus is simulated using a SQLite table.
- The cache is an in-memory cache instead of Redis.
- Rate limiting is in-memory and resets when the app restarts.
- The application is not yet deployed online.
- CDN, WAF, DDoS protection, and load balancing are not implemented locally.
- Docker and Kubernetes are not yet used.
- Customer order page UI can still be improved to look more like a real client-facing website.

---

## Future Improvements Based on Proposed Architecture

Future improvements will focus on expanding the local prototype into a more production-ready version of the proposed scalable FinMark architecture.

Recommended future improvements:

- Replace SQLite with separate service databases.
- Replace in-memory cache with Redis.
- Replace SQLite event_bus table with a real message broker.
- Add real payment gateway integration.
- Add email notifications for order confirmation.
- Add order status updates.
- Add customer order history.
- Add employee role-specific dashboards.
- Improve the customer service order UI.
- Add stronger security controls and MFA.
- Add Docker containerization.
- Add Kubernetes deployment.
- Add CDN, WAF, and DDoS protection.
- Add load balancing and HTTPS.
- Add Prometheus and Grafana monitoring.
- Add alert pipeline for failures and high traffic.

---

## How to Run the Project

1. Open the project folder in VS Code.


2. Activate the virtual environment:

   .venv\Scripts\activate

3. Install the required packages:

   pip install -r requirements.txt

4. Run the FastAPI server:

   python -m uvicorn app.main:app --reload

5. Open the browser and go to:

   http://127.0.0.1:8000

6. Register a user, log in, and test the prototype.

---

## How to Run Tests

Run this command:

   python -m pytest

Expected result:

   27 passed, 1 warning

---

## Demo Guide

Recommended demo flow:

1. Show the login page.
2. Show register validation error.
3. Register a customer account.
4. Log in as customer.
5. Show customer redirected to the service order page.
6. Submit a service order.
7. Log in as an employee.
8. Show the dashboard updated with order and payment data.
9. Open Orders page.
10. Open Services page.
11. Open Payments page.
12. Open Reports page.
13. Open Monitoring page.
14. Show /api/system/health.
15. Show Pytest result.
