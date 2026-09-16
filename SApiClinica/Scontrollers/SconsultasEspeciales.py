from fastapi import HTTPException, status

from Sdatabase.Sconexion import s_obtener_conexion


# =========================================================
# HISTORIAL DE CONSULTAS DE UN PACIENTE
# =========================================================

def s_historial_paciente(s_id_paciente: int):

    s_conexion = s_obtener_conexion()

    try:

        s_cursor = s_conexion.cursor()

        # -------------------------------------------------
        # Verificar que el paciente exista
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT id_paciente
            FROM pacientes
            WHERE id_paciente = %s;
        """, (s_id_paciente,))

        s_paciente = s_cursor.fetchone()

        if not s_paciente:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El paciente no existe"
            )

        # -------------------------------------------------
        # Consultar historial
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT
                co.id_consulta,
                co.id_cita,
                co.fecha,
                co.diagnostico,
                co.observaciones,
                co.tratamiento,
                ci.hora,
                m.nombres,
                m.apellidos
            FROM consultas co
            INNER JOIN citas ci
                ON co.id_cita = ci.id_cita
            INNER JOIN medicos m
                ON ci.id_medico = m.id_medico
            WHERE ci.id_paciente = %s
            ORDER BY co.fecha DESC;
        """, (s_id_paciente,))

        s_resultados = s_cursor.fetchall()

        s_historial = []

        for s_fila in s_resultados:

            s_historial.append({
                "id_consulta": s_fila[0],
                "id_cita": s_fila[1],
                "fecha": s_fila[2],
                "diagnostico": s_fila[3],
                "observaciones": s_fila[4],
                "tratamiento": s_fila[5],
                "hora": s_fila[6],
                "medico": f"{s_fila[7]} {s_fila[8]}"
            })

        return {
            "id_paciente": s_id_paciente,
            "total_consultas": len(s_historial),
            "historial": s_historial
        }

    finally:

        s_conexion.close()


# =========================================================
# CITAS DE UN PACIENTE
# =========================================================

def s_citas_paciente(s_id_paciente: int):

    s_conexion = s_obtener_conexion()

    try:

        s_cursor = s_conexion.cursor()

        # -------------------------------------------------
        # Verificar paciente
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT id_paciente
            FROM pacientes
            WHERE id_paciente = %s;
        """, (s_id_paciente,))

        s_paciente = s_cursor.fetchone()

        if not s_paciente:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El paciente no existe"
            )

        # -------------------------------------------------
        # Consultar citas
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT
                ci.id_cita,
                ci.fecha,
                ci.hora,
                ci.motivo,
                ci.estado,
                m.id_medico,
                m.nombres,
                m.apellidos
            FROM citas ci
            INNER JOIN medicos m
                ON ci.id_medico = m.id_medico
            WHERE ci.id_paciente = %s
            ORDER BY ci.fecha, ci.hora;
        """, (s_id_paciente,))

        s_resultados = s_cursor.fetchall()

        s_citas = []

        for s_fila in s_resultados:

            s_citas.append({
                "id_cita": s_fila[0],
                "fecha": s_fila[1],
                "hora": s_fila[2],
                "motivo": s_fila[3],
                "estado": s_fila[4],
                "id_medico": s_fila[5],
                "medico": f"{s_fila[6]} {s_fila[7]}"
            })

        return {
            "id_paciente": s_id_paciente,
            "total_citas": len(s_citas),
            "citas": s_citas
        }

    finally:

        s_conexion.close()


# =========================================================
# CITAS DE UN MÉDICO
# =========================================================

def s_citas_medico(s_id_medico: int):

    s_conexion = s_obtener_conexion()

    try:

        s_cursor = s_conexion.cursor()

        # -------------------------------------------------
        # Verificar médico
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT id_medico
            FROM medicos
            WHERE id_medico = %s;
        """, (s_id_medico,))

        s_medico = s_cursor.fetchone()

        if not s_medico:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El médico no existe"
            )

        # -------------------------------------------------
        # Consultar citas del médico
        # -------------------------------------------------

        s_cursor.execute("""
            SELECT
                ci.id_cita,
                ci.fecha,
                ci.hora,
                ci.motivo,
                ci.estado,
                p.id_paciente,
                p.nombres,
                p.apellidos
            FROM citas ci
            INNER JOIN pacientes p
                ON ci.id_paciente = p.id_paciente
            WHERE ci.id_medico = %s
            ORDER BY ci.fecha, ci.hora;
        """, (s_id_medico,))

        s_resultados = s_cursor.fetchall()

        s_citas = []

        for s_fila in s_resultados:

            s_citas.append({
                "id_cita": s_fila[0],
                "fecha": s_fila[1],
                "hora": s_fila[2],
                "motivo": s_fila[3],
                "estado": s_fila[4],
                "id_paciente": s_fila[5],
                "paciente": f"{s_fila[6]} {s_fila[7]}"
            })

        return {
            "id_medico": s_id_medico,
            "total_citas": len(s_citas),
            "citas": s_citas
        }

    finally:

        s_conexion.close()