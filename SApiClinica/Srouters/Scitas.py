from fastapi import APIRouter, status
from fastapi import Depends

from Smiddlewares.Sjwt import s_verificar_token

from Scontrollers.Scitas import (
    s_listar_citas,
    s_obtener_cita,
    s_crear_cita,
    s_actualizar_cita,
    s_eliminar_cita
)

from Sschemas.Scita import (
    SCitaCrear,
    SCitaActualizar
)


s_router_citas = APIRouter(
    prefix="/citas",
    tags=["Citas"],
    dependencies=[Depends(s_verificar_token)]
)


@s_router_citas.get(
    "",
    status_code=status.HTTP_200_OK
)
def s_listar():

    return s_listar_citas()


@s_router_citas.get(
    "/{s_id_cita}",
    status_code=status.HTTP_200_OK
)
def s_obtener(
    s_id_cita: int
):

    return s_obtener_cita(
        s_id_cita
    )


@s_router_citas.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def s_crear(
    s_cita: SCitaCrear
):

    return s_crear_cita(
        s_cita
    )


@s_router_citas.put(
    "/{s_id_cita}",
    status_code=status.HTTP_200_OK
)
def s_actualizar(
    s_id_cita: int,
    s_cita: SCitaActualizar
):

    return s_actualizar_cita(
        s_id_cita,
        s_cita
    )


@s_router_citas.delete(
    "/{s_id_cita}",
    status_code=status.HTTP_200_OK
)
def s_eliminar(
    s_id_cita: int
):

    return s_eliminar_cita(
        s_id_cita
    )