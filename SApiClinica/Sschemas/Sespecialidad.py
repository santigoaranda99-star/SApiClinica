from pydantic import BaseModel


class SEspecialidadCrear(BaseModel):

    nombre: str
    descripcion: str | None = None
    estado: str = "Activo"


class SEspecialidadActualizar(BaseModel):

    nombre: str
    descripcion: str | None = None
    estado: str = "Activo"