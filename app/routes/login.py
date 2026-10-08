from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.depends import get_usuario_repositorio

router = APIRouter(
    prefix="/login",
)

templates = Jinja2Templates(directory="templates")

@router.get("", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})

@router.post("", response_class=HTMLResponse)
async def login(
    usuario_repositorio: Annotated[UsuarioRepositorio, Depends(get_usuario_repositorio)],
    request: Request,
    email: Annotated[str, Form()],
    senha: Annotated[str, Form()],
):
    usuario = await usuario_repositorio.listar_usuario(email, senha)
    if usuario:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="session_token", value="token-senha", httponly=True)
        return response

    return templates.TemplateResponse(request, "login.html", {
        "request": request,
        "email": email,
        "error": "Credenciais inválidas"}, status_code=401)
