from fastapi import Request
from fastapi.responses  import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_path = request.url.path

        if request_path.startswith("/login") or request_path.startswith("/registro") or request_path.startswith("/static"):
            return await call_next(request)

        token = request.cookies.get("session_token")
        # Verifica se o usuário está autenticado
        if token != "token-senha":
            # Redireciona para a página de login se não estiver autenticado
            return RedirectResponse(url="/login", status_code=303)
        
        return await call_next(request)