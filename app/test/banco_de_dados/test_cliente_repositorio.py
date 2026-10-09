import pytest
from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.models.client import Client, ClientCreate

@pytest.fixture
def cliente_repositorio(mock_banco_dados):
    return ClienteRepositorio(mock_banco_dados)

class TestClienteRepositorio:
    @pytest.mark.asyncio
    async def test_listar_clientes(self, cliente_repositorio, mock_banco_dados):
        # Simula o banco devolvendo duas linhas
        mock_banco_dados.cursor.fetchall.return_value = [
            (1, "João", "joao@example.com", "(11) 1111-1111"),
            (2, "Maria", "maria@example.com", "(11) 2222-2222"),
        ]

        clientes = await cliente_repositorio.listar_clientes()

        assert clientes == [
            Client(id_=1, nome="João", email="joao@example.com", telefone="(11) 1111-1111"),
            Client(id_=2, nome="Maria", email="maria@example.com", telefone="(11) 2222-2222"),
        ]

    @pytest.mark.asyncio
    async def test_obter_cliente(self, cliente_repositorio, mock_banco_dados):
        # Simula o banco encontrando o cliente
        mock_banco_dados.cursor.fetchone.return_value = (1, "João", "joao@example.com", "(11) 1111-1111")

        cliente = await cliente_repositorio.obter_cliente(1)

        assert cliente == Client(id_=1, nome="João", email="joao@example.com", telefone="(11) 1111-1111")
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "SELECT id, nome, email, telefone FROM clients WHERE id = ?", (1,)
        )

    @pytest.mark.asyncio
    async def test_obter_cliente_inexistente(self, cliente_repositorio, mock_banco_dados):
        # Simula o banco sem nenhuma linha para esse id
        mock_banco_dados.cursor.fetchone.return_value = None

        cliente = await cliente_repositorio.obter_cliente(99)

        assert cliente is None

    @pytest.mark.asyncio
    async def test_create_client(self, cliente_repositorio, mock_banco_dados):
        # Simula o id gerado pelo banco no INSERT
        mock_banco_dados.cursor.lastrowid = 10
        novo_cliente = ClientCreate(nome="Teste", email="teste@example.com", telefone="123456789")

        cliente = await cliente_repositorio.create_client(novo_cliente)

        assert cliente == Client(id_=10, nome="Teste", email="teste@example.com", telefone="123456789")
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "INSERT INTO clients (nome, email, telefone) VALUES (?, ?, ?)",
            ("Teste", "teste@example.com", "123456789"),
        )
