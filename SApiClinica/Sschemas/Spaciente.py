from datetime import date

from pydantic import BaseModel, EmailStr


class SPacienteCrear(BaseModel):

    identificacion: str
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    telefono: str | None = None
    correo: EmailStr | None = None
    direccion: str | None = None
    estado: str = "Activo"


class SPacienteActualizar(BaseModel):

    identificacion: str
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    telefono: str | None = None
    correo: EmailStr | None = None
    direccion: str | None = None
    estado: str = "Activo"