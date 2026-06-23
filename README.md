# **FinMark Milestone 2: Prototype**

## **Project Overview**
FinMark is a software development prototype based on the proposed system architecture for a secure and scalable platform. For Milestone 2, the prototype focuses on one working core feature: a role-based user login and dashboard access module.

The project includes a working frontend, backend APIs, local database storage, authentication, protected routes, and service placeholders that represent the main services from the proposed architecture.

## **Purpose of the Prototype**

The purpose of this prototype is to create a minimum functional version of the platform. This version demonstrates how users can register, log in, receive authentication access, and view a protected dashboard.

## **Tools and Technologies Used**
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

## **What Was Set Up and Why**

A Python virtual environment was created to keep the project dependencies organized. FastAPI was used for the backend because it is lightweight and suitable for building APIs. SQLite was used as the local database because it is simple and does not require a separate database server.

HTML, CSS, Bootstrap, and JavaScript were used for the frontend. HTML structures the pages, CSS customizes the design, Bootstrap helps create a responsive modern layout, and JavaScript connects the frontend pages to the backend APIs.

## **Core Feature Developed**

The main core feature is the role-based user login and dashboard access module.

The user can:

Register an account
Log in using email and password
Receive a JWT authentication token
Access a protected dashboard
View dashboard data based on role and department
Log out from the system

## **Frontend Implementation**

The frontend includes three main pages:

Register page
Login page
Dashboard page

The Register page sends user information to the backend. The Login page sends credentials to the backend and stores the JWT token in browser localStorage. The Dashboard page uses the saved token to request protected dashboard data from the backend API.

## **Backend and API Implementation**

The backend was built using FastAPI. The API acts as the bridge between the frontend and backend. The frontend does not directly access the database. Instead, it sends requests to the backend API, and the backend handles validation, authentication, database access, and responses.

## **Database Implementation**

SQLite was used as the local database. The database stores registered user accounts with the following information:

User ID
Name
Email
Hashed password
Role
Department

Passwords are stored as hashed values instead of plain text. This improves basic security in the prototype.

## **Alignment with Proposed System Architecture**

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

## **Testing**

The prototype was tested through browser testing by registering a user, logging in, and accessing the dashboard. API testing can also be done using Postman. A Pytest test file is included to check basic system health, invalid login handling, protected dashboard access, and service status.

## **Challenges Encountered**

Some challenges encountered during development included setting up the project structure, connecting the frontend to the backend APIs, handling JWT authentication, checking if the database saved registered users correctly, and fixing a FastAPI template rendering issue.

Another challenge was making the prototype match the proposed architecture while still keeping it realistic for Milestone 2.

## **What Worked**

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

## **What Needs Refinement**

The current prototype already demonstrates the some of the Milestone 2 feature: role-based user login and protected dashboard access. However, it still needs refinement to better match the full proposed system architecture and the FinMark problem statement.

First, the current Order, Product, Payment, and Financial services are still placeholder services using sample data. These should be improved into non-static services that use real database records. The system should include actual order records, product inventory data, payment records, and financial summary data instead of only static responses.

Second, the prototype should include a minimal customer order placement module. The current system mainly supports employee users such as COO, admin, finance, operations, and staff. To connect the prototype more closely to the problem statement about increasing online orders, a customer-facing order API or page should be added where customers can place sample orders.

Third, the database should be expanded. The current SQLite database mainly stores authentication users. To better represent the proposed Database Layer, additional tables should be added for orders, products, payments, audit logs, and service events. These tables can simulate the Order DB, Product DB, Payment DB, Auth DB, Audit Log Storage, and Async Message Bus in the local prototype.

Fourth, the system should improve service communication. Instead of services only returning placeholder data, the Order Service, Product Service, and Payment Service should communicate through a simulated event bus. For example, when an order is placed, the system can record an order_placed event, update product inventory, create a payment record, and record the activity in audit logs.

Lastly, the API Gateway behavior should be strengthened. The system already includes JWT authentication, RBAC, and request logging, but it should still add rate limiting, circuit breaker or fallback behavior, audit logging, and better service health checking. The current in-memory cache should also be improved or later replaced with Redis Cache.

## **Future Improvements Based on Proposed Architecture**

Future improvements will focus on expanding the local prototype into a more complete version of the proposed scalable FinMark architecture.

The Application Layer should be improved by converting the placeholder services into real service modules. The Order Service should handle customer order placement and order status updates. The Product Service should manage product and inventory records. The Payment Service should simulate payment processing and payment status. The Auth Service should continue handling login, JWT token generation, and role-based access.

An Async Message Bus should be added so services can communicate through events instead of only direct function calls. Events such as order_placed, inventory_updated, payment_done, and payment_failed can help simulate how the services work together in a scalable system.

Redis Cache should be added as the production caching layer. In the current prototype, a simple in-memory cache is used to reduce dashboard loading time. In the future, Redis can store frequently requested dashboard, order, and product data so the system can better support high concurrent usage.

Audit Log Storage should be added to record important system activities such as user registration, login attempts, dashboard access, order placement, payment updates, and failed service actions. This will improve traceability, security monitoring, and system accountability.

The Database Layer should be expanded into separate service databases such as Order DB, Product DB, Payment DB, and Auth DB. In the local prototype, this can first be simulated using separate SQLite tables, but in a production setup, each service can have its own dedicated database with backup, read replica, and failover support.

The Edge Layer should later include CDN, WAF, and DDoS protection. The Load Balancer layer should include round-robin routing, health checks, and SSL/TLS termination for HTTPS. Monitoring should also be improved using monitoring agents, Prometheus, Grafana, and an Alert Pipeline. For deployment, Docker and Kubernetes can be used for service containers, scaling, and high availability.

## **How to Run the Project**
1. Open the project folder in VS Code.
2. Activate the virtual environment: .venv\Scripts\activate
3. Install the required packages: pip install -r requirements.txt
4. Run the FastAPI server: python -m uvicorn app.main:app --reload
5. Open the browser and go to: http://127.0.0.1:8000
6. Register a user, log in, and access the dashboard.
