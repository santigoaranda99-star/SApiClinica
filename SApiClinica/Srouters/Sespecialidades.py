from fastapi import APIRouter, status
from fastapi import Depends

from Smiddlewares.Sjwt import s_verificar_token

from Scontrollers.Sespecialidades import (
    s_listar_especialidades,
    s_obtener_especialidad,
    s_crear_especialidad,
    s_actualizar_especialidad,
    s_eliminar_especialidad
)

from Sschemas.Sespecialidad import (
    SEspecialidadCrear,
    SEspecialidadActualizar
)


s_router_especialidades = APIRouter(
    prefix="/especialidades",
    tags=["Especialidades"],
    dependencies=[Depends(s_verificar_token)]
)


@s_router_especialidades.get(
    "",
    status_code=status.HTTP_200_OK
)
def s_listar():

    return s_listar_especialidades()


@s_router_especialidades.get(
    "/{s_id_especialidad}",
    status_code=status.HTTP_200_OK
)
def s_obtener(
    s_id_especialidad: int
):

    return s_obtener_especialidad(
        s_id_especialidad
    )


@s_router_especialidades.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def s_crear(
    s_especialidad: SEspecialidadCrear
):

    return s_crear_especialidad(
        s_especialidad
    )


@s_router_especialidades.put(
    "/{s_id_especialidad}",
    status_code=status.HTTP_200_OK
)
def s_actualizar(
    s_id_especialidad: int,
    s_especialidad: SEspecialidadActualizar
):

    return s_actualizar_especialidad(
        s_id_especialidad,
        s_especialidad
    )


@s_router_especialidades.delete(
    "/{s_id_especialidad}",
    status_code=status.HTTP_200_OK
)
def s_eliminar(
    s_id_especialidad: int
):

    return s_eliminar_especialidad(
        s_id_especialidad
    )