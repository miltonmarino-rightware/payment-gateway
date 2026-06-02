import uuid
from starlette.middleware.base import BaseHTTPMiddleware
class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id=request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id=request_id
        request.state.client_ip=request.client.host if request.client else "unknown"
        request.state.user_agent=request.headers.get("user-agent", "unknown")
        response=await call_next(request)
        response.headers["x-request-id"]=request_id
        return response
