from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes.api_v1 import api

USERNAME = 'admin'
PASSWORD = 'admin'
security = HTTPBasic()

app = FastAPI(
    title='Crm market API',
    contact={
        'name': "ASILBEK",
        'url': 'https://t.me/murojaat13_bot',
    },
    description="Boss username:  "
                "Boss password: "
                "Admin username: "
                "Admin password: ",
    docs_url=None,
    redoc_url=None,
)


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")


@app.get("/redoc", include_in_schema=False)
def custom_redoc(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="ReDoc Documentation"
    )

if not os.path.exists("images"):
    os.makedirs("images")

app.include_router(api, prefix='/api/v1')

app.mount(
    "/images/",
    StaticFiles(directory=os.path.join(os.getcwd(), "images")),
    name="images"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
