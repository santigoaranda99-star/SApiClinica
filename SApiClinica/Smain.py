from fastapi import FastAPI

from Srouters.Spacientes import s_router_pacientes
from Srouters.Sespecialidades import s_router_especialidades
from Srouters.Smedicos import s_router_medicos
from Srouters.Scitas import s_router_citas
from Srouters.Sconsultas import s_router_consultas
from Srouters.Slogin import s_router_login


s_app = FastAPI(
    title="SAPI Clínica",
    description="API REST para la gestión de información de una clínica",
    version="1.0.0"
)


s_app.include_router(
    s_router_pacientes
)

s_app.include_router(
    s_router_especialidades
)

s_app.include_router(
    s_router_medicos
)

s_app.include_router(
    s_router_citas
)

s_app.include_router(
    s_router_consultas
)

s_app.include_router(
    s_router_login
)


@s_app.get("/")
def s_inicio():

    return {
        "mensaje": "API de la Clínica funcionando correctamente"
    }