from fastapi import HTTPException, status

from Sconfig import (
    S_LOGIN_CORREO,
    S_LOGIN_PASSWORD
)

from Sschemas.Slogin import SLogin

from Smiddlewares.Sjwt import s_crear_token


# =========================================================
# LOGIN
# =========================================================

def s_login(s_datos: SLogin):

    # -----------------------------------------------------
    # Verificar correo
    # -----------------------------------------------------

    if s_datos.correo != S_LOGIN_CORREO:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    # -----------------------------------------------------
    # Verificar contraseña
    # -----------------------------------------------------

    if s_datos.password != S_LOGIN_PASSWORD:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    # -----------------------------------------------------
    # Crear token
    # -----------------------------------------------------

    s_token = s_crear_token({
        "sub": s_datos.correo
    })

    return {

        "mensaje": "Inicio de sesión exitoso",

        "access_token": s_token,

        "token_type": "bearer",

        "usuario": {
            "correo": s_datos.correo
        }
    }