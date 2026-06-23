**FinMark Milestone 2: Role-Based Fast Dashboard Prototype**

**Project Overview**
FinMark is a software development prototype based on the proposed system architecture for a secure and scalable platform. For Milestone 2, the prototype focuses on one working core feature: a role-based user login and dashboard access module.

The project includes a working frontend, backend APIs, local database storage, authentication, protected routes, and service placeholders that represent the main services from the proposed architecture.

**Purpose of the Prototype**

The purpose of this prototype is to create a minimum functional version of the platform. Instead of building the full production system immediately, this version demonstrates how users can register, log in, receive authentication access, and view a protected dashboard.

This satisfies the Software Development Track requirement by providing a working login module with both frontend and backend logic.

**Tools and Technologies Used**
Python
FastAPI
SQLite
HTML
CSS
Bootstrap
JavaScript
VS Code
GitHub
Postman
Pytest

**What Was Set Up and Why**

A Python virtual environment was created to keep the project dependencies organized. FastAPI was used for the backend because it is lightweight and suitable for building APIs. SQLite was used as the local database because it is simple and does not require a separate database server.

HTML, CSS, Bootstrap, and JavaScript were used for the frontend. HTML structures the pages, CSS customizes the design, Bootstrap helps create a responsive modern layout, and JavaScript connects the frontend pages to the backend APIs.

**Core Feature Developed**

The main core feature is the role-based user login and dashboard access module.

The user can:

Register an account
Log in using email and password
Receive a JWT authentication token
Access a protected dashboard
View dashboard data based on role and department
Log out from the system

**Frontend Implementation**

The frontend includes three main pages:

Register page
Login page
Dashboard page

The Register page sends user information to the backend. The Login page sends credentials to the backend and stores the JWT token in browser localStorage. The Dashboard page uses the saved token to request protected dashboard data from the backend API.

**Backend and API Implementation**

The backend was built using FastAPI. The API acts as the bridge between the frontend and backend. The frontend does not directly access the database. Instead, it sends requests to the backend API, and the backend handles validation, authentication, database access, and responses.

Main APIs created:

POST /api/auth/register - registers a new user
POST /api/auth/login - logs in a user and returns a JWT token
GET /api/auth/me - checks the current logged-in user
GET /api/dashboard/summary - returns protected dashboard data
GET /api/system/services - shows system service status
GET /api/orders/summary - shows order service data
GET /api/products/summary - shows product service data
GET /api/payments/summary - shows payment service data
GET /api/financials/summary - shows financial service data

**Database Implementation**

SQLite was used as the local database. The database stores registered user accounts with the following information:

User ID
Name
Email
Hashed password
Role
Department

Passwords are stored as hashed values instead of plain text. This improves basic security in the prototype.

**Alignment with Proposed System Architecture**

The current prototype is aligned with the proposed architecture in a simplified local version.

Implemented or simulated components:

Web Application: Register, Login, and Dashboard pages
API Gateway Layer: FastAPI routes
JWT Validation and RBAC: JWT token authentication and role-based access
Request Logging: API response time logging
Auth Service: Working registration and login service
Order Service: Placeholder service
Product Service: Placeholder service
Payment Service: Placeholder service
Financial Service: Placeholder service
Auth Database: SQLite users table
Cache: Simple in-memory dashboard cache
Monitoring: Response time shown in terminal and dashboard
Service Health Check: System service status endpoint

**Testing**

The prototype was tested through browser testing by registering a user, logging in, and accessing the dashboard. API testing can also be done using Postman. A Pytest test file is included to check basic system health, invalid login handling, protected dashboard access, and service status.

**Challenges Encountered**

Some challenges encountered during development included setting up the project structure, connecting the frontend to the backend APIs, handling JWT authentication, checking if the database saved registered users correctly, and fixing a FastAPI template rendering issue.

Another challenge was making the prototype match the proposed architecture while still keeping it realistic for Milestone 2.

**What Worked**

The following parts are working:

User registration
User login
Password hashing
JWT token generation
Protected dashboard access
SQLite database storage
Frontend and backend connection
Dashboard API data loading
Placeholder service integration
Response time display
Logout function

**What Needs Refinement**

The current prototype still needs refinement to better match the full proposed architecture. The placeholder services should be improved into non-static services that use real records. Audit logging, rate limiting, circuit breaker behavior, and stronger API Gateway behavior should also be added.

The current in-memory cache should eventually be replaced with Redis Cache, and the single SQLite database should be expanded into separate service databases such as Order DB, Product DB, Payment DB, and Auth DB.

**Future Improvements Based on Proposed Architecture**

Future improvements include adding the Edge Layer with CDN, WAF, and DDoS protection. The Load Balancer layer should include round-robin routing, health checks, and SSL/TLS termination for HTTPS.

The Application Layer should be improved by making the Order, Product, Payment, and Auth services more complete. An Async Message Bus should be added so services can communicate using events such as order_placed and payment_done.

The system should also include Redis Cache, Audit Log Storage, separate databases per service, monitoring agents, Prometheus and Grafana monitoring, an Alert Pipeline, and Docker/Kubernetes deployment for scalability and high availability.

**How to Run the Project**
Open the project folder in VS Code.
Activate the virtual environment:
.venv\Scripts\activate
Install the required packages:
pip install -r requirements.txt
Run the FastAPI server:
python -m uvicorn app.main:app --reload
Open the browser and go to:
http://127.0.0.1:8000
Register a user, log in, and access the dashboard.
