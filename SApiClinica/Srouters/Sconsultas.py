from fastapi import APIRouter, status
from fastapi import Depends

from Smiddlewares.Sjwt import s_verificar_token

from Scontrollers.Sconsultas import (
    s_listar_consultas,
    s_obtener_consulta,
    s_crear_consulta,
    s_actualizar_consulta,
    s_eliminar_consulta
)

from Sschemas.Sconsulta import (
    SConsultaCrear,
    SConsultaActualizar
)


s_router_consultas = APIRouter(
    prefix="/consultas",
    tags=["Consultas"],
    dependencies=[Depends(s_verificar_token)]
)


# =========================================================
# GET /consultas
# =========================================================

@s_router_consultas.get(
    "",
    status_code=status.HTTP_200_OK
)
def s_listar():

    return s_listar_consultas()


# =========================================================
# GET /consultas/{id}
# =========================================================

@s_router_consultas.get(
    "/{s_id_consulta}",
    status_code=status.HTTP_200_OK
)
def s_obtener(s_id_consulta: int):

    return s_obtener_consulta(s_id_consulta)


# =========================================================
# POST /consultas
# =========================================================

@s_router_consultas.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def s_crear(s_consulta: SConsultaCrear):

    return s_crear_consulta(s_consulta)


# =========================================================
# PUT /consultas/{id}
# =========================================================

@s_router_consultas.put(
    "/{s_id_consulta}",
    status_code=status.HTTP_200_OK
)
def s_actualizar(
    s_id_consulta: int,
    s_consulta: SConsultaActualizar
):

    return s_actualizar_consulta(
        s_id_consulta,
        s_consulta
    )


# =========================================================
# DELETE /consultas/{id}
# =========================================================

@s_router_consultas.delete(
    "/{s_id_consulta}",
    status_code=status.HTTP_200_OK
)
def s_eliminar(s_id_consulta: int):

    return s_eliminar_consulta(s_id_consulta)