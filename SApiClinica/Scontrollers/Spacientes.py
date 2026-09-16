from fastapi import HTTPException, status

from Sdatabase.Sconexion import s_obtener_conexion
from Sschemas.Spaciente import (
    SPacienteCrear,
    SPacienteActualizar
)


def s_listar_pacientes():

    s_conexion = s_obtener_conexion()

    try:
        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT
                    id_paciente,
                    identificacion,
                    nombres,
                    apellidos,
                    fecha_nacimiento,
                    telefono,
                    correo,
                    direccion,
                    estado
                FROM pacientes
                ORDER BY id_paciente;
            """)

            s_columnas = [
                "id_paciente",
                "identificacion",
                "nombres",
                "apellidos",
                "fecha_nacimiento",
                "telefono",
                "correo",
                "direccion",
                "estado"
            ]

            s_resultados = s_cursor.fetchall()

            return [
                dict(zip(s_columnas, s_fila))
                for s_fila in s_resultados
            ]

    finally:
        s_conexion.close()


def s_obtener_paciente(s_id_paciente: int):

    s_conexion = s_obtener_conexion()

    try:
        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT
                    id_paciente,
                    identificacion,
                    nombres,
                    apellidos,
                    fecha_nacimiento,
                    telefono,
                    correo,
                    direccion,
                    estado
                FROM pacientes
                WHERE id_paciente = %s;
            """, (s_id_paciente,))

            s_resultado = s_cursor.fetchone()

            if s_resultado is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paciente no encontrado"
                )

            s_columnas = [
                "id_paciente",
                "identificacion",
                "nombres",
                "apellidos",
                "fecha_nacimiento",
                "telefono",
                "correo",
                "direccion",
                "estado"
            ]

            return dict(zip(s_columnas, s_resultado))

    finally:
        s_conexion.close()


def s_crear_paciente(s_paciente: SPacienteCrear):

    s_conexion = s_obtener_conexion()

    try:
        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT id_paciente
                FROM pacientes
                WHERE identificacion = %s;
            """, (s_paciente.identificacion,))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La identificación ya está registrada"
                )

            s_cursor.execute("""
                INSERT INTO pacientes (
                    identificacion,
                    nombres,
                    apellidos,
                    fecha_nacimiento,
                    telefono,
                    correo,
                    direccion,
                    estado
                )
                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                RETURNING
                    id_paciente,
                    identificacion,
                    nombres,
                    apellidos,
                    fecha_nacimiento,
                    telefono,
                    correo,
                    direccion,
                    estado;
            """, (
                s_paciente.identificacion,
                s_paciente.nombres,
                s_paciente.apellidos,
                s_paciente.fecha_nacimiento,
                s_paciente.telefono,
                s_paciente.correo,
                s_paciente.direccion,
                s_paciente.estado
            ))

            s_resultado = s_cursor.fetchone()

            s_conexion.commit()

            s_columnas = [
                "id_paciente",
                "identificacion",
                "nombres",
                "apellidos",
                "fecha_nacimiento",
                "telefono",
                "correo",
                "direccion",
                "estado"
            ]

            return dict(zip(s_columnas, s_resultado))

    finally:
        s_conexion.close()


def s_actualizar_paciente(
    s_id_paciente: int,
    s_paciente: SPacienteActualizar
):

    s_conexion = s_obtener_conexion()

    try:
        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT id_paciente
                FROM pacientes
                WHERE id_paciente = %s;
            """, (s_id_paciente,))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paciente no encontrado"
                )

            s_cursor.execute("""
                SELECT id_paciente
                FROM pacientes
                WHERE identificacion = %s
                AND id_paciente <> %s;
            """, (
                s_paciente.identificacion,
                s_id_paciente
            ))

            if s_cursor.fetchone() is not None:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La identificación ya pertenece a otro paciente"
                )

            s_cursor.execute("""
                UPDATE pacientes
                SET
                    identificacion = %s,
                    nombres = %s,
                    apellidos = %s,
                    fecha_nacimiento = %s,
                    telefono = %s,
                    correo = %s,
                    direccion = %s,
                    estado = %s
                WHERE id_paciente = %s
                RETURNING
                    id_paciente,
                    identificacion,
                    nombres,
                    apellidos,
                    fecha_nacimiento,
                    telefono,
                    correo,
                    direccion,
                    estado;
            """, (
                s_paciente.identificacion,
                s_paciente.nombres,
                s_paciente.apellidos,
                s_paciente.fecha_nacimiento,
                s_paciente.telefono,
                s_paciente.correo,
                s_paciente.direccion,
                s_paciente.estado,
                s_id_paciente
            ))

            s_resultado = s_cursor.fetchone()

            s_conexion.commit()

            s_columnas = [
                "id_paciente",
                "identificacion",
                "nombres",
                "apellidos",
                "fecha_nacimiento",
                "telefono",
                "correo",
                "direccion",
                "estado"
            ]

            return dict(zip(s_columnas, s_resultado))

    finally:
        s_conexion.close()


def s_eliminar_paciente(s_id_paciente: int):

    s_conexion = s_obtener_conexion()

    try:
        with s_conexion.cursor() as s_cursor:

            s_cursor.execute("""
                SELECT id_paciente
                FROM pacientes
                WHERE id_paciente = %s;
            """, (s_id_paciente,))

            if s_cursor.fetchone() is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paciente no encontrado"
                )

            s_cursor.execute("""
                DELETE FROM pacientes
                WHERE id_paciente = %s;
            """, (s_id_paciente,))

            s_conexion.commit()

            return {
                "mensaje": "Paciente eliminado correctamente"
            }

    finally:
        s_conexion.close()