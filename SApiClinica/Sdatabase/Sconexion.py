import os

import psycopg
from dotenv import load_dotenv


load_dotenv("S.env")


def s_obtener_conexion():
    s_conexion = psycopg.connect(
        host=os.getenv("SDB_HOST"),
        port=os.getenv("SDB_PORT"),
        dbname=os.getenv("SDB_NAME"),
        user=os.getenv("SDB_USER"),
        password=os.getenv("SDB_PASSWORD")
    )

    return s_conexion