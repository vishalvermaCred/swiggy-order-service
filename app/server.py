import logging
from os import getenv

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.context import app_context
from app.database import Postgres
from app.exceptions import HTTPBaseException, MissingEnvConfigsException
from app.middlewares import LoginMiddleware
from app.routes import router
from app.settings import BASE_ROUTE, LOG_LEVEL, SERVICE_NAME, ORDER_DB_CONFIGS


# Intializing app
app = FastAPI(docs_url=f"{BASE_ROUTE}/docs", redoc_url=f"{BASE_ROUTE}/redocs")
app.add_middleware(LoginMiddleware)


async def _init_routers():
    app.include_router(router, prefix=BASE_ROUTE)


extra = {"app_name": SERVICE_NAME}
logging.basicConfig(level=LOG_LEVEL, format=f"%(asctime)s {SERVICE_NAME} %(levelname)s : %(message)s")
logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(logger, extra)


async def verify_env_configs():
    mandatory_variables = [
        "ENV",
        "APP_NAME",
        "BASE_ROUTE",
        "LOG_LEVEL",
        "SERVICE_NAME",
        "DB_HOST",
        "DB_PORT",
        "ORDER_DB_USER",
        "ORDER_DB_PASSWORD",
        "ORDER_DB_NAME",
    ]
    missing_configs = []
    for key in mandatory_variables:
        if not getenv(key):
            missing_configs.append(key)
    if missing_configs:
        return False, missing_configs

    return True, []


async def _init_db():
    db_conf = ORDER_DB_CONFIGS.copy()
    kwargs = {
        "database": db_conf["NAME"],
        "host": db_conf["HOST"],
        "port": db_conf["PORT"],
        "user": db_conf["USER"],
        "password": db_conf["PASSWORD"],
    }
    database = Postgres(**kwargs)
    await database.connect()
    return database


@app.on_event("startup")
async def startup_event():
    logger.info("SERVER STARTING...")
    env_verified, missing_configs = await verify_env_configs()
    if not env_verified:
        raise MissingEnvConfigsException(parameters=",".join(missing_configs))
    logger.info("🟢 Env Verified...")
    await _init_routers()
    app_context.db = await _init_db()
    logger.info("🟢 Postgres DB Connected...")


@app.on_event("shutdown")
async def shutdown_event():
    await app_context.db.close()
    logger.info("🟢 App Shutdown Completed.")


@app.exception_handler(413)
def request_entity_too_large():
    return JSONResponse(content={"message": "File Too Large"}, status_code=413)


@app.exception_handler(422)
def unprocessable_request_entity():
    return JSONResponse(content={"message": "Unprocessable Entity"}, status_code=413)


@app.exception_handler(HTTPBaseException)
async def http_base_exception_handler(request: Request, exc: HTTPBaseException):
    message = exc.message

    return JSONResponse(
        status_code=exc.code,
        content={
            "success": False,
            "message": message,
            "data": {},
        },
    )


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(request: Request, exc: RequestValidationError):
    response_dict = {"success": False, "message": "Invalid Payload", "data": {}}
    try:
        response_dict["data"] = exc.errors()
    except Exception as e:
        logger.exception(e)

    return JSONResponse(status_code=400, content=response_dict)
