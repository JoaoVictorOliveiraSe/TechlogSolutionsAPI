from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import client, login, registro
from app.depends import banco_de_dados

templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    banco_de_dados.inicializar_banco()
    yield

app = FastAPI(
    title="Techlog Solutions API",
    description="CRM para Techlog Solutions",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(client.router)
app.include_router(client.frontend_router)
app.include_router(login.router)
app.include_router(registro.router)

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.get("/", response_class=HTMLResponse)
async def front_page(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request, "title": "Techlog Solutions CRM", "version": "1.0.0"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)