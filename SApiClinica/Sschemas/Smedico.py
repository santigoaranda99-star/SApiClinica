from pydantic import BaseModel, EmailStr


class SMedicoCrear(BaseModel):

    identificacion: str
    nombres: str
    apellidos: str
    id_especialidad: int
    telefono: str | None = None
    correo: EmailStr | None = None
    estado: str = "Activo"


class SMedicoActualizar(BaseModel):

    identificacion: str
    nombres: str
    apellidos: str
    id_especialidad: int
    telefono: str | None = None
    correo: EmailStr | None = None
    estado: str = "Activo"