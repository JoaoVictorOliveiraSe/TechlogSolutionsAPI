from app.banco_de_dados.local import BancoDeDados
from app.models.client import Client, ClientCreate

class ClienteRepositorio:
    def __init__(self, banco_de_dados: BancoDeDados):
        self.bd = banco_de_dados

    async def listar_clientes(self) -> list[Client]:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clients")
            rows = cursor.fetchall()
            clientes = [Client(id_=row[0], nome=row[1], email=row[2], telefone=row[3]) for row in rows]
            return clientes

    async def obter_cliente(self, client_id: int) -> Client | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clients WHERE id = ?", (client_id,))
            row = cursor.fetchone()
            if row:
                return Client(id_=row[0], nome=row[1], email=row[2], telefone=row[3])
            return None

    async def create_client(self, client: ClientCreate) -> Client:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO clients (nome, email, telefone) VALUES (?, ?, ?)",
                (client.nome, client.email, client.telefone)
            )
            return Client(id_=cursor.lastrowid, nome=client.nome, email=client.email, telefone=client.telefone)

    async def update_client(self, client_id: int, client: ClientCreate) -> Client | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE clients SET nome = ?, email = ?, telefone = ? WHERE id = ?", 
                           (client.nome, client.email, client.telefone, client_id))
            if cursor.rowcount > 0:
                return Client(id_=client_id, nome=client.nome, email=client.email, telefone=client.telefone)
            return None

    async def delete_client(self, client_id: int) -> bool:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            return cursor.rowcount > 0