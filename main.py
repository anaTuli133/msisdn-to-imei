from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routes import router

from db import fetch_table  
import table_draw  # noqa: F401

app = FastAPI(
    title="MSISDN to IMEI API",
    description="3rd party authorized access — Basic Auth required",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Static files - CSS/JS 
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory setup
templates = Jinja2Templates(directory="templates")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes include
app.include_router(router, prefix="/api")

# --- Frontend Routes ---

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def login_page(request: Request): 
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard(request: Request):
   
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/view-table", response_class=HTMLResponse, include_in_schema=False)
async def view_table(request: Request, search: str = Query(None)):
    cols, rows = fetch_table(search_query=search)
    return templates.TemplateResponse(
        "CDR14_IMEI_table.html", 
        {
            "request": request, 
            "cols": cols, 
            "rows": rows, 
            "search_query": search
        }
    )