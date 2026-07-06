import time

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.utils.resilience import is_rate_limited

from app.database import init_db
from app.features.auth.auth_routes import router as auth_router
from app.features.dashboard.dashboard_routes import router as dashboard_router
from app.features.system_routes import router as system_router
from app.features.monitoring_routes import router as monitoring_router
from app.features.orders.order_routes import router as order_router

@asynccontextmanager
async def server_lifetime(app : FastAPI):
    # eq to on_event("startup")
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    init_db()

    print("Initialization complete")
    yield # eq to on_event("shutdown")
    print("Shutdown complete")

templates = Jinja2Templates(directory="app/templates")
app = FastAPI(title="FinMark Milestone 2 API Prototype", lifespan=server_lifetime)


@app.middleware("http")
async def api_gateway_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    path = request.url.path

    if path.startswith("/api"):
        client_host = request.client.host if request.client else "unknown"
        client_id = f"{client_host}:{path}"

        if is_rate_limited(client_id):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please wait before trying again.",
                    "resilience_feature": "API Gateway rate limiting"
                }
            )

    response = await call_next(request)

    process_time = round((time.perf_counter() - start_time) * 1000, 2)

    print(f"{request.method} {path} completed in {process_time}ms")

    response.headers["X-Process-Time-ms"] = str(process_time)
    response.headers["X-Prototype-Gateway"] = "FinMark API Gateway Middleware"
    response.headers["X-Rate-Limit-Policy"] = "120 requests per 60 seconds per API route"

    return response


app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(system_router, prefix="/api", tags=["Architecture Services"])
app.include_router(monitoring_router, prefix="/api", tags=["Monitoring"])
app.include_router(order_router, prefix="/api", tags=["Service Orders"])

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )

@app.get("/order", response_class=HTMLResponse)
def order_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="order.html"
    )

@app.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="data_page.html",
        context={
            "page_title": "Orders",
            "page_description": "View FinMark customer service orders from the database.",
            "page_type": "orders"
        }
    )


@app.get("/products", response_class=HTMLResponse)
def products_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="data_page.html",
        context={
            "page_title": "Services",
            "page_description": "View the FinMark service catalog used by the Product Service.",
            "page_type": "products"
        }
    )


@app.get("/payments", response_class=HTMLResponse)
def payments_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="data_page.html",
        context={
            "page_title": "Payments",
            "page_description": "View payment records created from customer service orders.",
            "page_type": "payments"
        }
    )


@app.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="data_page.html",
        context={
            "page_title": "Reports",
            "page_description": "Review database-backed financial, order, payment, and service summaries.",
            "page_type": "reports"
        }
    )


@app.get("/monitoring", response_class=HTMLResponse)
def monitoring_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="data_page.html",
        context={
            "page_title": "Monitoring",
            "page_description": "View system health, audit logs, and event bus activity.",
            "page_type": "monitoring"
        }
    )

@app.get("/health")
def health_check():
    return {
        "message": "FinMark backend is running",
        "status": "healthy"
    }