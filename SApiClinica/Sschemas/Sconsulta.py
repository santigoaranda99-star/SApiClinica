from pydantic import BaseModel
from datetime import date


class SConsultaCrear(BaseModel):

    id_cita: int
    fecha: date
    motivo: str
    diagnostico: str
    observaciones: str
    tratamiento: str


class SConsultaActualizar(BaseModel):

    id_cita: int
    fecha: date
    motivo: str
    diagnostico: str
    observaciones: str
    tratamiento: str