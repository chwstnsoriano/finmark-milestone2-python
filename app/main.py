import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.features.auth.auth_routes import router as auth_router
from app.features.dashboard.dashboard_routes import router as dashboard_router
from app.features.system_routes import router as system_router

app = FastAPI(title="FinMark Milestone 2 API Prototype")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def startup_event():
    init_db()


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = round((time.perf_counter() - start_time) * 1000, 2)
    print(f"{request.method} {request.url.path} completed in {process_time}ms")

    response.headers["X-Process-Time-ms"] = str(process_time)

    return response


app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(system_router, prefix="/api", tags=["Architecture Services"])


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


@app.get("/health")
def health_check():
    return {
        "message": "FinMark backend is running",
        "status": "healthy"
    }