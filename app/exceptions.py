from http.client import HTTPException


class MissingEnvConfigsException(Exception):
    def __init__(self, parameters):
        self.code = 501
        self.message = f"Missing Env Configs: {parameters}"

    def __str__(self):
        return self.message


class HTTPBaseException(HTTPException):
    code = 500
    message = "Helicarrier Base Exception"
