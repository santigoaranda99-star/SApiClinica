from fastapi import HTTPException, status

from Sdatabase.Sconexion import s_obtener_conexion

from Sschemas.Sespecialidad import (
    SEspecialidadCrear,
    SEspecialidadActualizar
)


def s_listar_especialidades():

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT
                    id_especialidad,
                    nombre,
                    descripcion,
                    estado
                FROM especialidades
                ORDER BY id_especialidad;
            """)

            s_resultados = s_cursor.fetchall()

            s_columnas = [
                "id_especialidad",
                "nombre",
                "descripcion",
                "estado"
            ]

            return [
                dict(zip(s_columnas, s_fila))
                for s_fila in s_resultados
            ]

    finally:

        s_conexion.close()


def s_obtener_especialidad(s_id_especialidad: int):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT
                    id_especialidad,
                    nombre,
                    descripcion,
                    estado
                FROM especialidades
                WHERE id_especialidad = %s;
            """, (s_id_especialidad,))

            s_resultado = s_cursor.fetchone()

            if s_resultado is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Especialidad no encontrada"
                )

            s_columnas = [
                "id_especialidad",
                "nombre",
                "descripcion",
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


def s_crear_especialidad(
    s_especialidad: SEspecialidadCrear
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT id_especialidad
                FROM especialidades
                WHERE LOWER(nombre) = LOWER(%s);
            """, (s_especialidad.nombre,))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La especialidad ya existe"
                )

            s_cursor.execute("""
                INSERT INTO especialidades (
                    nombre,
                    descripcion,
                    estado
                )
                VALUES (
                    %s,
                    %s,
                    %s
                )
                RETURNING
                    id_especialidad,
                    nombre,
                    descripcion,
                    estado;
            """, (
                s_especialidad.nombre,
                s_especialidad.descripcion,
                s_especialidad.estado
            ))

            s_resultado = s_cursor.fetchone()

            s_conexion.commit()

            s_columnas = [
                "id_especialidad",
                "nombre",
                "descripcion",
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


def s_actualizar_especialidad(
    s_id_especialidad: int,
    s_especialidad: SEspecialidadActualizar
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT id_especialidad
                FROM especialidades
                WHERE id_especialidad = %s;
            """, (s_id_especialidad,))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Especialidad no encontrada"
                )

            s_cursor.execute("""
                SELECT id_especialidad
                FROM especialidades
                WHERE LOWER(nombre) = LOWER(%s)
                AND id_especialidad <> %s;
            """, (
                s_especialidad.nombre,
                s_id_especialidad
            ))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otra especialidad con ese nombre"
                )

            s_cursor.execute("""
                UPDATE especialidades
                SET
                    nombre = %s,
                    descripcion = %s,
                    estado = %s
                WHERE id_especialidad = %s
                RETURNING
                    id_especialidad,
                    nombre,
                    descripcion,
                    estado;
            """, (
                s_especialidad.nombre,
                s_especialidad.descripcion,
                s_especialidad.estado,
                s_id_especialidad
            ))

            s_resultado = s_cursor.fetchone()

            s_conexion.commit()

            s_columnas = [
                "id_especialidad",
                "nombre",
                "descripcion",
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


def s_eliminar_especialidad(
    s_id_especialidad: int
):

    s_conexion = s_obtener_conexion()

    try:

        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT id_especialidad
                FROM especialidades
                WHERE id_especialidad = %s;
            """, (s_id_especialidad,))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Especialidad no encontrada"
                )

            s_cursor.execute("""
                SELECT id_medico
                FROM medicos
                WHERE id_especialidad = %s
                LIMIT 1;
            """, (s_id_especialidad,))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "No se puede eliminar la especialidad "
                        "porque tiene médicos asociados"
                    )
                )

            s_cursor.execute("""
                DELETE FROM especialidades
                WHERE id_especialidad = %s;
            """, (s_id_especialidad,))

            s_conexion.commit()

            return {
                "mensaje": "Especialidad eliminada correctamente"
            }

    finally:

        s_conexion.close()