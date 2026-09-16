from fastapi import HTTPException, status

from Sdatabase.Sconexion import s_obtener_conexion

from Sschemas.Sconsulta import (
    SConsultaCrear,
    SConsultaActualizar
)


# =========================================================
# LISTAR CONSULTAS
# =========================================================

def s_listar_consultas():

    s_conexion = s_obtener_conexion()

    try:

        s_cursor = s_conexion.cursor()

        s_cursor.execute("""
            SELECT
                id_consulta,
                id_cita,
                fecha,
                motivo,
                diagnostico,
                observaciones,
                tratamiento
            FROM consultas
            ORDER BY fecha DESC;
        """)

        s_consultas = s_cursor.fetchall()

        s_resultado = []

        for s_consulta in s_consultas:

            s_resultado.append({
                "id_consulta": s_consulta[0],
                "id_cita": s_consulta[1],
                "fecha": s_consulta[2],
                "motivo": s_consulta[3],
                "diagnostico": s_consulta[4],
                "observaciones": s_consulta[5],
                "tratamiento": s_consulta[6]
            })

        return s_resultado

    finally:

        s_conexion.close()


# =========================================================
# OBTENER CONSULTA POR ID
# =========================================================

def s_obtener_consulta(s_id_consulta: int):

    s_conexion = s_obtener_conexion()

    try:

        s_cursor = s_conexion.cursor()

        s_cursor.execute("""
            SELECT
                id_consulta,
                id_cita,
                fecha,
                motivo,
                diagnostico,
                observaciones,
                tratamiento
            FROM consultas
            WHERE id_consulta = %s;
        """, (s_id_consulta,))

        s_consulta = s_cursor.fetchone()

        if not s_consulta:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consulta no encontrada"
            )

        return {
            "id_consulta": s_consulta[0],
            "id_cita": s_consulta[1],
            "fecha": s_consulta[2],
            "motivo": s_consulta[3],
            "diagnostico": s_consulta[4],
            "observaciones": s_consulta[5],
            "tratamiento": s_consulta[6]
        }

    finally:

        s_conexion.close()


# =========================================================
# CREAR CONSULTA
# =========================================================

def s_crear_consulta(s_consulta: SConsultaCrear):

    s_conexion = s_obtener_conexion()

    try:

        s_cursor = s_conexion.cursor()

        # -------------------------------------------------
        # Verificar que la cita exista
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT id_cita
            FROM citas
            WHERE id_cita = %s;
        """, (s_consulta.id_cita,))

        s_cita = s_cursor.fetchone()

        if not s_cita:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La cita indicada no existe"
            )

        # -------------------------------------------------
        # Verificar que la cita no tenga consulta
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT id_consulta
            FROM consultas
            WHERE id_cita = %s;
        """, (s_consulta.id_cita,))

        s_consulta_existente = s_cursor.fetchone()

        if s_consulta_existente:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta cita ya tiene una consulta registrada"
            )

        # -------------------------------------------------
        # Crear consulta
        # -------------------------------------------------

        s_cursor.execute("""
            INSERT INTO consultas (
                id_cita,
                fecha,
                motivo,
                diagnostico,
                observaciones,
                tratamiento
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING
                id_consulta,
                id_cita,
                fecha,
                motivo,
                diagnostico,
                observaciones,
                tratamiento;
        """, (
            s_consulta.id_cita,
            s_consulta.fecha,
            s_consulta.motivo,
            s_consulta.diagnostico,
            s_consulta.observaciones,
            s_consulta.tratamiento
        ))

        s_nueva_consulta = s_cursor.fetchone()

        s_conexion.commit()

        return {
            "mensaje": "Consulta creada correctamente",
            "consulta": {
                "id_consulta": s_nueva_consulta[0],
                "id_cita": s_nueva_consulta[1],
                "fecha": s_nueva_consulta[2],
                "motivo": s_nueva_consulta[3],
                "diagnostico": s_nueva_consulta[4],
                "observaciones": s_nueva_consulta[5],
                "tratamiento": s_nueva_consulta[6]
            }
        }

    finally:

        s_conexion.close()


# =========================================================
# ACTUALIZAR CONSULTA
# =========================================================

def s_actualizar_consulta(
    s_id_consulta: int,
    s_consulta: SConsultaActualizar
):

    s_conexion = s_obtener_conexion()

    try:

        s_cursor = s_conexion.cursor()

        # -------------------------------------------------
        # Verificar que la consulta exista
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT id_consulta
            FROM consultas
            WHERE id_consulta = %s;
        """, (s_id_consulta,))

        s_consulta_existente = s_cursor.fetchone()

        if not s_consulta_existente:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consulta no encontrada"
            )

        # -------------------------------------------------
        # Verificar que la cita exista
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT id_cita
            FROM citas
            WHERE id_cita = %s;
        """, (s_consulta.id_cita,))

        s_cita = s_cursor.fetchone()

        if not s_cita:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La cita indicada no existe"
            )

        # -------------------------------------------------
        # Verificar que otra consulta no use esa cita
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT id_consulta
            FROM consultas
            WHERE id_cita = %s
            AND id_consulta <> %s;
        """, (
            s_consulta.id_cita,
            s_id_consulta
        ))

        s_otra_consulta = s_cursor.fetchone()

        if s_otra_consulta:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La cita ya está asociada a otra consulta"
            )

        # -------------------------------------------------
        # Actualizar consulta
        # -------------------------------------------------

        s_cursor.execute("""
            UPDATE consultas
            SET
                id_cita = %s,
                fecha = %s,
                motivo = %s,
                diagnostico = %s,
                observaciones = %s,
                tratamiento = %s
            WHERE id_consulta = %s
            RETURNING
                id_consulta,
                id_cita,
                fecha,
                motivo,
                diagnostico,
                observaciones,
                tratamiento;
        """, (
            s_consulta.id_cita,
            s_consulta.fecha,
            s_consulta.motivo,
            s_consulta.diagnostico,
            s_consulta.observaciones,
            s_consulta.tratamiento,
            s_id_consulta
        ))

        s_actualizada = s_cursor.fetchone()

        s_conexion.commit()

        return {
            "mensaje": "Consulta actualizada correctamente",
            "consulta": {
                "id_consulta": s_actualizada[0],
                "id_cita": s_actualizada[1],
                "fecha": s_actualizada[2],
                "motivo": s_actualizada[3],
                "diagnostico": s_actualizada[4],
                "observaciones": s_actualizada[5],
                "tratamiento": s_actualizada[6]
            }
        }

    finally:

        s_conexion.close()


# =========================================================
# ELIMINAR CONSULTA
# =========================================================

def s_eliminar_consulta(s_id_consulta: int):

    s_conexion = s_obtener_conexion()

    try:

        s_cursor = s_conexion.cursor()

        s_cursor.execute("""
            SELECT id_consulta
            FROM consultas
            WHERE id_consulta = %s;
        """, (s_id_consulta,))

        s_consulta = s_cursor.fetchone()

        if not s_consulta:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consulta no encontrada"
            )

        s_cursor.execute("""
            DELETE FROM consultas
            WHERE id_consulta = %s;
        """, (s_id_consulta,))

        s_conexion.commit()

        return {
            "mensaje": "Consulta eliminada correctamente"
        }

    finally:

        s_conexion.close()