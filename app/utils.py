from http import HTTPStatus
from fastapi.responses import JSONResponse

from app.constants import ResponseKeys


async def generate_response(success, message, code=HTTPStatus.OK, data=None):
    response = {
        ResponseKeys.SUCCESS: success,
        ResponseKeys.MESSAGE: message,
        ResponseKeys.DATA: data or {},
        ResponseKeys.ERROR: {},
    }
    api_response = JSONResponse(response, code)
    return api_response
