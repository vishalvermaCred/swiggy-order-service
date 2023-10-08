import logging
from http import HTTPStatus
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from app.settings import SERVICE_NAME, LOG_LEVEL

extra = {"app_name": SERVICE_NAME}
logging.basicConfig(level=LOG_LEVEL, format=f"%(asctime)s {SERVICE_NAME} %(levelname)s : %(message)s")
logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(logger, extra)


class LoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        login_required_response = await self.login_required(request)
        logger.info(f"Login Required Response: {login_required_response}")

        if login_required_response[1] is not HTTPStatus.OK.value:
            return JSONResponse(content=login_required_response[0], status_code=login_required_response[1])

        response = await call_next(request)
        return response

    async def login_required(self, request):
        # TODO: login logic goes here
        return {"message": "valid user"}, 200
