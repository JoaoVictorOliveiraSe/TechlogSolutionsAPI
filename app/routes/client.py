from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.models.client import Client, ClientCreate
from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.depends import get_cliente_repositorio

router = APIRouter(
    prefix="/clients",
)

@router.get("/", response_model=list[Client])
async def list_clients(cliente_repositorio:Annotated[ClienteRepositorio, Depends(get_cliente_repositorio)]):
    return await cliente_repositorio.listar_clientes()

@router.get("/{client_id}", response_model=Client)
async def obter_client(cliente_repositorio:Annotated[ClienteRepositorio, Depends(get_cliente_repositorio)], client_id: int):
    client = await cliente_repositorio.obter_cliente(client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client

@router.post("/", response_model=Client, status_code=201)
async def create_client(cliente_repositorio:Annotated[ClienteRepositorio, Depends(get_cliente_repositorio)], client: ClientCreate):
    return await cliente_repositorio.create_client(client)

@router.put("/{client_id}", response_model=Client)
async def update_client(cliente_repositorio:Annotated[ClienteRepositorio, Depends(get_cliente_repositorio)], client_id: int, client: ClientCreate):
    updated_client = await cliente_repositorio.update_client(client_id, client)

    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")

    return updated_client

@router.delete("/{client_id}", status_code=204)
async def delete_client(cliente_repositorio:Annotated[ClienteRepositorio, Depends(get_cliente_repositorio)], client_id: int):
    deleted = await cliente_repositorio.delete_client(client_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")

    return None