from app.banco_de_dados.local import BancoDeDados
from app.models.usuario import Usuario, UsuarioCreate

class UsuarioRepositorio:
    def __init__(self, banco_de_dados: BancoDeDados):
        self.bd = banco_de_dados

    async def listar_usuario(self, email: str, senha: str) -> Usuario | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
            row = cursor.fetchone()
            if row:
                return Usuario(id_=row[0], nome=row[1], email=row[2])
            return None

    async def create_usuario(self, usuario: UsuarioCreate) -> Usuario:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (usuario.nome, usuario.email, usuario.senha)
            )
            id_ = cursor.lastrowid
            return Usuario(id_=id_, nome=usuario.nome, email=usuario.email)

    async def obter_usuario(self, email: str) -> Usuario | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return Usuario(id_=row[0], nome=row[1], email=row[2])
            return None