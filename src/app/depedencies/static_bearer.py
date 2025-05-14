from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param

from app.config import setting
from app.execptions.auth import CredentialNotFound, InvalidCredentials


class StaticBearer(HTTPBearer):
    def __init__(self):
        super().__init__()
        self.model.bearerFormat = "Bearer"

    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        secret_key: list[str] = setting.SECRET_KEY.split(",")

        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (scheme and credentials):
            raise CredentialNotFound()

        try:
            token = credentials.split(" ")[1]
        except IndexError:
            token = credentials

        if token not in secret_key:
            raise InvalidCredentials()

        return credentials
