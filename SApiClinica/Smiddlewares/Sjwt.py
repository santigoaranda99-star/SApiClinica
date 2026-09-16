from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from jose import jwt, JWTError

from Sconfig import (
    S_SECRET_KEY,
    S_ALGORITHM,
    S_ACCESS_TOKEN_EXPIRE_MINUTES
)


# =========================================================
# CONFIGURACIÓN BEARER
# =========================================================

s_security = HTTPBearer()


# =========================================================
# CREAR TOKEN JWT
# =========================================================

def s_crear_token(s_datos: dict):

    s_datos_token = s_datos.copy()

    s_expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=S_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    s_datos_token.update({
        "exp": s_expiracion
    })

    s_token = jwt.encode(
        s_datos_token,
        S_SECRET_KEY,
        algorithm=S_ALGORITHM
    )

    return s_token


# =========================================================
# VERIFICAR TOKEN JWT
# =========================================================

def s_verificar_token(
    s_credenciales: HTTPAuthorizationCredentials = Depends(
        s_security
    )
):

    s_token = s_credenciales.credentials

    try:

        s_payload = jwt.decode(
            s_token,
            S_SECRET_KEY,
            algorithms=[S_ALGORITHM]
        )

        s_usuario = s_payload.get("sub")

        if s_usuario is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        return s_usuario

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )