from pydantic import BaseModel

class Client(BaseModel):
    id_: int
    nome: str
    email: str
    telefone: str

class ClientCreate(BaseModel):
    nome: str
    email: str
    telefone: str
    