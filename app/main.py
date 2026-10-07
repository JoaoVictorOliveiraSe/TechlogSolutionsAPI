from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes import client
from app.depends import banco_de_dados


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

app.include_router(client.router)

@app.get("/")
async def health_check():
    return {"status": "OK"}

@app.get("/front", response_class=HTMLResponse)
async def front_page():
    html_content = """
    <html>
        <head>
            <title>Techlog Solutions API</title>
        </head>
        <body>
            <h1>Welcome to Techlog Solutions API</h1>
            <p>This is the front page of the Techlog Solutions API.</p>
            <p>Status: <strong> Operacional </strong></p>
        </body>
    </html>
"""
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)