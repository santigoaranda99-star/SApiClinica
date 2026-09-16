from fastapi import APIRouter, status
from fastapi import Depends
from Scontrollers.SconsultasEspeciales import (
    s_citas_medico
)

from Smiddlewares.Sjwt import s_verificar_token

from Scontrollers.Smedicos import (
    s_listar_medicos,
    s_obtener_medico,
    s_crear_medico,
    s_actualizar_medico,
    s_eliminar_medico
)

from Sschemas.Smedico import (
    SMedicoCrear,
    SMedicoActualizar
)


s_router_medicos = APIRouter(
    prefix="/medicos",
    tags=["Médicos"],
    dependencies=[Depends(s_verificar_token)]
)


@s_router_medicos.get(
    "",
    status_code=status.HTTP_200_OK
)
def s_listar():

    return s_listar_medicos()


@s_router_medicos.get(
    "/{s_id_medico}",
    status_code=status.HTTP_200_OK
)
def s_obtener(
    s_id_medico: int
):

    return s_obtener_medico(
        s_id_medico
    )


@s_router_medicos.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def s_crear(
    s_medico: SMedicoCrear
):

    return s_crear_medico(
        s_medico
    )


@s_router_medicos.put(
    "/{s_id_medico}",
    status_code=status.HTTP_200_OK
)
def s_actualizar(
    s_id_medico: int,
    s_medico: SMedicoActualizar
):

    return s_actualizar_medico(
        s_id_medico,
        s_medico
    )


@s_router_medicos.delete(
    "/{s_id_medico}",
    status_code=status.HTTP_200_OK
)
def s_eliminar(
    s_id_medico: int
):

    return s_eliminar_medico(
        s_id_medico
    )
    
# =========================================================
# CITAS DEL MÉDICO
# =========================================================

@s_router_medicos.get(
    "/{s_id_medico}/citas",
    status_code=status.HTTP_200_OK
)
def s_citas(
    s_id_medico: int
):

    return s_citas_medico(
        s_id_medico
    )