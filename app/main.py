from app.core.compat import *  # This must be the first import
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.routes import payments

app = FastAPI(
    title="Transbank Payment API",
    description="API for handling payments using Transbank Webpay Plus",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(payments.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    with open("app/static/index.html") as f:
        return f.read()

@app.get("/payment-result", response_class=HTMLResponse)
async def payment_result(request: Request, token_ws: str = None):
    """Handle the return from Transbank payment"""
    # Serve the dedicated payment result page
    with open("app/static/payment-result.html") as f:
        return f.read()

