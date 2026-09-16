from pydantic import BaseModel


class SLogin(BaseModel):

    correo: str

    password: str