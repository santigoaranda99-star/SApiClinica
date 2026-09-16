from fastapi import HTTPException, status

from Sdatabase.Sconexion import s_obtener_conexion

from Sschemas.Smedico import (
    SMedicoCrear,
    SMedicoActualizar
)


def s_listar_medicos():

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT
                    id_medico,
                    identificacion,
                    nombres,
                    apellidos,
                    id_especialidad,
                    telefono,
                    correo,
                    estado
                FROM medicos
                ORDER BY id_medico;
            """)

            s_resultados = s_cursor.fetchall()

            s_columnas = [
                "id_medico",
                "identificacion",
                "nombres",
                "apellidos",
                "id_especialidad",
                "telefono",
                "correo",
                "estado"
            ]

            return [
                dict(zip(s_columnas, s_fila))
                for s_fila in s_resultados
            ]

    finally:

        s_conexion.close()


def s_obtener_medico(s_id_medico: int):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT
                    id_medico,
                    identificacion,
                    nombres,
                    apellidos,
                    id_especialidad,
                    telefono,
                    correo,
                    estado
                FROM medicos
                WHERE id_medico = %s;
            """, (s_id_medico,))

            s_resultado = s_cursor.fetchone()

            if s_resultado is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Médico no encontrado"
                )

            s_columnas = [
                "id_medico",
                "identificacion",
                "nombres",
                "apellidos",
                "id_especialidad",
                "telefono",
                "correo",
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


def s_crear_medico(
    s_medico: SMedicoCrear
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            # ==========================================
            # 1. VERIFICAR IDENTIFICACIÓN
            # ==========================================

            s_cursor.execute("""
                SELECT id_medico
                FROM medicos
                WHERE identificacion = %s;
            """, (s_medico.identificacion,))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La identificación ya está registrada"
                )

            # ==========================================
            # 2. VERIFICAR ESPECIALIDAD
            # ==========================================

            s_cursor.execute("""
                SELECT id_especialidad
                FROM especialidades
                WHERE id_especialidad = %s;
            """, (s_medico.id_especialidad,))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La especialidad indicada no existe"
                )

            # ==========================================
            # 3. INSERTAR MÉDICO
            # ==========================================

            s_cursor.execute("""
                INSERT INTO medicos (
                    identificacion,
                    nombres,
                    apellidos,
                    id_especialidad,
                    telefono,
                    correo,
                    estado
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING
                    id_medico,
                    identificacion,
                    nombres,
                    apellidos,
                    id_especialidad,
                    telefono,
                    correo,
                    estado;
            """, (
                s_medico.identificacion,
                s_medico.nombres,
                s_medico.apellidos,
                s_medico.id_especialidad,
                s_medico.telefono,
                s_medico.correo,
                s_medico.estado
            ))

            s_resultado = s_cursor.fetchone()

            s_conexion.commit()

            s_columnas = [
                "id_medico",
                "identificacion",
                "nombres",
                "apellidos",
                "id_especialidad",
                "telefono",
                "correo",
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


def s_actualizar_medico(
    s_id_medico: int,
    s_medico: SMedicoActualizar
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            # ==========================================
            # 1. VERIFICAR QUE EL MÉDICO EXISTA
            # ==========================================

            s_cursor.execute("""
                SELECT id_medico
                FROM medicos
                WHERE id_medico = %s;
            """, (s_id_medico,))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Médico no encontrado"
                )

            # ==========================================
            # 2. VERIFICAR IDENTIFICACIÓN
            # ==========================================

            s_cursor.execute("""
                SELECT id_medico
                FROM medicos
                WHERE identificacion = %s
                AND id_medico <> %s;
            """, (
                s_medico.identificacion,
                s_id_medico
            ))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La identificación ya pertenece a otro médico"
                )

            # ==========================================
            # 3. VERIFICAR ESPECIALIDAD
            # ==========================================

            s_cursor.execute("""
                SELECT id_especialidad
                FROM especialidades
                WHERE id_especialidad = %s;
            """, (s_medico.id_especialidad,))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La especialidad indicada no existe"
                )

            # ==========================================
            # 4. ACTUALIZAR MÉDICO
            # ==========================================

            s_cursor.execute("""
                UPDATE medicos
                SET
                    identificacion = %s,
                    nombres = %s,
                    apellidos = %s,
                    id_especialidad = %s,
                    telefono = %s,
                    correo = %s,
                    estado = %s
                WHERE id_medico = %s
                RETURNING
                    id_medico,
                    identificacion,
                    nombres,
                    apellidos,
                    id_especialidad,
                    telefono,
                    correo,
                    estado;
            """, (
                s_medico.identificacion,
                s_medico.nombres,
                s_medico.apellidos,
                s_medico.id_especialidad,
                s_medico.telefono,
                s_medico.correo,
                s_medico.estado,
                s_id_medico
            ))

            s_resultado = s_cursor.fetchone()

            s_conexion.commit()

            s_columnas = [
                "id_medico",
                "identificacion",
                "nombres",
                "apellidos",
                "id_especialidad",
                "telefono",
                "correo",
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


def s_eliminar_medico(
    s_id_medico: int
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            # ==========================================
            # 1. VERIFICAR QUE EXISTA
            # ==========================================

            s_cursor.execute("""
                SELECT id_medico
                FROM medicos
                WHERE id_medico = %s;
            """, (s_id_medico,))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Médico no encontrado"
                )

            # ==========================================
            # 2. VERIFICAR SI TIENE CITAS
            # ==========================================

            s_cursor.execute("""
                SELECT id_cita
                FROM citas
                WHERE id_medico = %s
                LIMIT 1;
            """, (s_id_medico,))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "No se puede eliminar el médico "
                        "porque tiene citas asociadas"
                    )
                )

            # ==========================================
            # 3. ELIMINAR
            # ==========================================

            s_cursor.execute("""
                DELETE FROM medicos
                WHERE id_medico = %s;
            """, (s_id_medico,))

            s_conexion.commit()

            return {
                "mensaje": "Médico eliminado correctamente"
            }

    finally:

        s_conexion.close()