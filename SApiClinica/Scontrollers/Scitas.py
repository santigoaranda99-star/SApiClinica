from fastapi import HTTPException, status

from Sdatabase.Sconexion import s_obtener_conexion

from Sschemas.Scita import (
    SCitaCrear,
    SCitaActualizar
)


# ==========================================================
# LISTAR CITAS
# ==========================================================

def s_listar_citas():

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT
                    id_cita,
                    id_paciente,
                    id_medico,
                    fecha,
                    hora,
                    motivo,
                    estado
                FROM citas
                ORDER BY fecha, hora;
            """)

            s_resultados = s_cursor.fetchall()

            s_columnas = [
                "id_cita",
                "id_paciente",
                "id_medico",
                "fecha",
                "hora",
                "motivo",
                "estado"
            ]

            return [
                dict(zip(s_columnas, s_fila))
                for s_fila in s_resultados
            ]

    finally:

        s_conexion.close()


# ==========================================================
# OBTENER CITA POR ID
# ==========================================================

def s_obtener_cita(
    s_id_cita: int
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT
                    id_cita,
                    id_paciente,
                    id_medico,
                    fecha,
                    hora,
                    motivo,
                    estado
                FROM citas
                WHERE id_cita = %s;
            """, (s_id_cita,))

            s_resultado = s_cursor.fetchone()

            if s_resultado is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cita no encontrada"
                )

            s_columnas = [
                "id_cita",
                "id_paciente",
                "id_medico",
                "fecha",
                "hora",
                "motivo",
                "estado"
            ]

            return dict(
                zip(
                    s_columnas,
                    s_resultado
                )
            )

    finally:

        s_conexion.close()


# ==========================================================
# CREAR CITA
# ==========================================================

def s_crear_cita(
    s_cita: SCitaCrear
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            # ------------------------------------------------
            # 1. VERIFICAR PACIENTE
            # ------------------------------------------------

            s_cursor.execute("""
                SELECT id_paciente
                FROM pacientes
                WHERE id_paciente = %s;
            """, (
                s_cita.id_paciente,
            ))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El paciente indicado no existe"
                )

            # ------------------------------------------------
            # 2. VERIFICAR MÉDICO
            # ------------------------------------------------

            s_cursor.execute("""
                SELECT id_medico
                FROM medicos
                WHERE id_medico = %s;
            """, (
                s_cita.id_medico,
            ))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El médico indicado no existe"
                )

            # ------------------------------------------------
            # 3. VERIFICAR DISPONIBILIDAD DEL MÉDICO
            # ------------------------------------------------

            s_cursor.execute("""
                SELECT id_cita
                FROM citas
                WHERE id_medico = %s
                AND fecha = %s
                AND hora = %s
                AND estado = 'Programada';
            """, (
                s_cita.id_medico,
                s_cita.fecha,
                s_cita.hora
            ))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "El médico ya tiene una cita "
                        "programada para esa fecha y hora"
                    )
                )

            # ------------------------------------------------
            # 4. INSERTAR CITA
            # ------------------------------------------------

            s_cursor.execute("""
                INSERT INTO citas (
                    id_paciente,
                    id_medico,
                    fecha,
                    hora,
                    motivo,
                    estado
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING
                    id_cita,
                    id_paciente,
                    id_medico,
                    fecha,
                    hora,
                    motivo,
                    estado;
            """, (
                s_cita.id_paciente,
                s_cita.id_medico,
                s_cita.fecha,
                s_cita.hora,
                s_cita.motivo,
                s_cita.estado
            ))

            s_resultado = s_cursor.fetchone()

            s_conexion.commit()

            s_columnas = [
                "id_cita",
                "id_paciente",
                "id_medico",
                "fecha",
                "hora",
                "motivo",
                "estado"
            ]

            return dict(
                zip(
                    s_columnas,
                    s_resultado
                )
            )

    finally:

        s_conexion.close()


# ==========================================================
# ACTUALIZAR CITA
# ==========================================================

def s_actualizar_cita(
    s_id_cita: int,
    s_cita: SCitaActualizar
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            # ------------------------------------------------
            # 1. VERIFICAR QUE LA CITA EXISTA
            # ------------------------------------------------

            s_cursor.execute("""
                SELECT id_cita
                FROM citas
                WHERE id_cita = %s;
            """, (
                s_id_cita,
            ))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cita no encontrada"
                )

            # ------------------------------------------------
            # 2. VERIFICAR PACIENTE
            # ------------------------------------------------

            s_cursor.execute("""
                SELECT id_paciente
                FROM pacientes
                WHERE id_paciente = %s;
            """, (
                s_cita.id_paciente,
            ))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El paciente indicado no existe"
                )

            # ------------------------------------------------
            # 3. VERIFICAR MÉDICO
            # ------------------------------------------------

            s_cursor.execute("""
                SELECT id_medico
                FROM medicos
                WHERE id_medico = %s;
            """, (
                s_cita.id_medico,
            ))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El médico indicado no existe"
                )

            # ------------------------------------------------
            # 4. VERIFICAR DISPONIBILIDAD
            # ------------------------------------------------

            s_cursor.execute("""
                SELECT id_cita
                FROM citas
                WHERE id_medico = %s
                AND fecha = %s
                AND hora = %s
                AND estado = 'Programada'
                AND id_cita <> %s;
            """, (
                s_cita.id_medico,
                s_cita.fecha,
                s_cita.hora,
                s_id_cita
            ))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "El médico ya tiene otra cita "
                        "programada para esa fecha y hora"
                    )
                )

            # ------------------------------------------------
            # 5. ACTUALIZAR
            # ------------------------------------------------

            s_cursor.execute("""
                UPDATE citas
                SET
                    id_paciente = %s,
                    id_medico = %s,
                    fecha = %s,
                    hora = %s,
                    motivo = %s,
                    estado = %s
                WHERE id_cita = %s
                RETURNING
                    id_cita,
                    id_paciente,
                    id_medico,
                    fecha,
                    hora,
                    motivo,
                    estado;
            """, (
                s_cita.id_paciente,
                s_cita.id_medico,
                s_cita.fecha,
                s_cita.hora,
                s_cita.motivo,
                s_cita.estado,
                s_id_cita
            ))

            s_resultado = s_cursor.fetchone()

            s_conexion.commit()

            s_columnas = [
                "id_cita",
                "id_paciente",
                "id_medico",
                "fecha",
                "hora",
                "motivo",
                "estado"
            ]

            return dict(
                zip(
                    s_columnas,
                    s_resultado
                )
            )

    finally:

        s_conexion.close()


# ==========================================================
# ELIMINAR CITA
# ==========================================================

def s_eliminar_cita(
    s_id_cita: int
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            # ------------------------------------------------
            # 1. VERIFICAR EXISTENCIA
            # ------------------------------------------------

            s_cursor.execute("""
                SELECT id_cita
                FROM citas
                WHERE id_cita = %s;
            """, (
                s_id_cita,
            ))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cita no encontrada"
                )

            # ------------------------------------------------
            # 2. ELIMINAR
            # ------------------------------------------------

            s_cursor.execute("""
                DELETE FROM citas
                WHERE id_cita = %s;
            """, (
                s_id_cita,
            ))

            s_conexion.commit()

            return {
                "mensaje": "Cita eliminada correctamente"
            }

    finally:

        s_conexion.close()