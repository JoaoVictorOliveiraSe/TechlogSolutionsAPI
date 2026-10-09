from contextlib import asynccontextmanager, contextmanager
from fastapi import FastAPI, Request
from unittest.mock import AsyncMock, MagicMock, Mock, patch
import pytest

@pytest.fixture
def mock_banco_dados():
    class MockBancoDados:
        def __init__(self):
            self.conexao = MagicMock()
            self.cursor = MagicMock()
            self.conexao.cursor.return_value = self.cursor

        @contextmanager
        def conectar(self):
            yield self.conexao

    return MockBancoDados()

@pytest.fixture
def mock_cliente_repositorio():
    mock_repo = Mock()
    mock_repo.obter_cliente = AsyncMock()
    mock_repo.create_cliente = AsyncMock()  
    return mock_repo

@pytest.fixture
def mock_usuario_repositorio():
    mock_repo = Mock()
    mock_repo.obter_usuario = AsyncMock()
    mock_repo.create_usuario = AsyncMock()  
    return mock_repo

@pytest.fixture
def mock_request():
    mock_request = Mock(spec=Request)
    mock_request.cookies = {}
    return mock_request