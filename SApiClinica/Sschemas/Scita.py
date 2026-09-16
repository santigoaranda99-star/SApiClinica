from pydantic import BaseModel
from datetime import date, time


class SCitaCrear(BaseModel):

    id_paciente: int
    id_medico: int
    fecha: date
    hora: time
    motivo: str | None = None
    estado: str = "Programada"


class SCitaActualizar(BaseModel):

    id_paciente: int
    id_medico: int
    fecha: date
    hora: time
    motivo: str | None = None
    estado: str = "Programada"