from fastapi import APIRouter, status, Depends
from Smiddlewares.Sjwt import s_verificar_token
from Scontrollers.SconsultasEspeciales import (
    s_historial_paciente,
    s_citas_paciente
)
from Scontrollers.Spacientes import (
    s_listar_pacientes,
    s_obtener_paciente,
    s_crear_paciente,
    s_actualizar_paciente,
    s_eliminar_paciente
)

from Sschemas.Spaciente import (
    SPacienteCrear,
    SPacienteActualizar
)


s_router_pacientes = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"],
    dependencies=[Depends(s_verificar_token)]
)


@s_router_pacientes.get(
    "",
    status_code=status.HTTP_200_OK
)
def s_listar():

    return s_listar_pacientes()


@s_router_pacientes.get(
    "/{s_id_paciente}",
    status_code=status.HTTP_200_OK
)
def s_obtener(s_id_paciente: int):

    return s_obtener_paciente(s_id_paciente)


@s_router_pacientes.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def s_crear(s_paciente: SPacienteCrear):

    return s_crear_paciente(s_paciente)


@s_router_pacientes.put(
    "/{s_id_paciente}",
    status_code=status.HTTP_200_OK
)
def s_actualizar(
    s_id_paciente: int,
    s_paciente: SPacienteActualizar
):

    return s_actualizar_paciente(
        s_id_paciente,
        s_paciente
    )


@s_router_pacientes.delete(
    "/{s_id_paciente}",
    status_code=status.HTTP_200_OK
)
def s_eliminar(s_id_paciente: int):

    return s_eliminar_paciente(s_id_paciente)

# =========================================================
# HISTORIAL MÉDICO DEL PACIENTE
# =========================================================

@s_router_pacientes.get(
    "/{s_id_paciente}/historial",
    status_code=status.HTTP_200_OK
)
def s_historial(
    s_id_paciente: int
):

    return s_historial_paciente(
        s_id_paciente
    )


# =========================================================
# CITAS DEL PACIENTE
# =========================================================

@s_router_pacientes.get(
    "/{s_id_paciente}/citas",
    status_code=status.HTTP_200_OK
)
def s_citas(
    s_id_paciente: int
):

    return s_citas_paciente(
        s_id_paciente
    )