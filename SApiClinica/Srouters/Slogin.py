from fastapi import APIRouter, status

from Scontrollers.Slogin import s_login

from Sschemas.Slogin import SLogin


s_router_login = APIRouter(
    prefix="/login",
    tags=["Autenticación"]
)


@s_router_login.post(
    "",
    status_code=status.HTTP_200_OK
)
def s_iniciar_sesion(
    s_datos: SLogin
):

    return s_login(s_datos)