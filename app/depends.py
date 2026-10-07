from typing import Annotated
from fastapi import Depends
from app.banco_de_dados.local import BancoDeDados
from app.banco_de_dados.cliente_repositorio import ClienteRepositorio

banco_de_dados = BancoDeDados()

def get_banco_de_dados() -> BancoDeDados:
    return banco_de_dados

def get_cliente_repositorio(
        banco_de_dados: Annotated[BancoDeDados, Depends(get_banco_de_dados)]
    )-> ClienteRepositorio:
    return ClienteRepositorio(banco_de_dados)