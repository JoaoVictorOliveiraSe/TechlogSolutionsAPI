from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.depends import get_usuario_repositorio
from app.models.usuario import UsuarioCreate

router = APIRouter(
    prefix="/registro",
)

templates = Jinja2Templates(directory="templates")

@router.get("", response_class=HTMLResponse)
async def registro_page(request: Request):
    return templates.TemplateResponse(request, "registro.html", {"request": request})

@router.post("", response_class=HTMLResponse)
async def registro(
    usuario_repositorio: Annotated[UsuarioRepositorio, Depends(get_usuario_repositorio)],
    request: Request,
    nome: Annotated[str, Form()],
    email: Annotated[str, Form()],
    senha: Annotated[str, Form()],
    confirma_senha: Annotated[str, Form()]
):
    if senha != confirma_senha:
        return templates.TemplateResponse(request, "registro.html", {
            "request": request,
            "error": "As senhas não coincidem",
            "nome": nome,
            "email": email,
        }, status_code=400)

    usuario_existente = await usuario_repositorio.obter_usuario(email)

    if usuario_existente:
        return templates.TemplateResponse(request, "registro.html", {
            "request": request,
            "error": "O email já está em uso",
            "nome": nome,
            "email": email,
        }, status_code=400)

    await usuario_repositorio.create_usuario(UsuarioCreate(nome=nome, email=email, senha=senha))

    return RedirectResponse(url="/login", status_code=303)