from fastapi import APIRouter
from app.db.database import Database
from app.models import Entrada, Proyecto

db = Database()
conn = db.conn
cursor = db.cursor
router = APIRouter()

@router.post('/registrar')
def registrar(entrada:Entrada):
    query = "INSERT INTO entrada (dinero, fecha, proyecto_id) VALUES (%s, %s, %s)"
    values = (entrada.dinero,entrada.fecha,entrada.proyecto_id)
    cursor.execute(query, values)
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    last_insert_id = cursor.fetchone()[0]
    entrada.id = last_insert_id
    
    query2 = "SELECT * FROM proyectos WHERE id = %s"
    cursor.execute(query2, [entrada.proyecto_id])
    diccionario = cursor.fetchone()
    entrada.proyecto = Proyecto.to_json(diccionario)
    return entrada

@router.post('/modificar')
def modificar(entrada: Entrada):
    query = "UPDATE entrada SET dinero = %s, fecha = %s, proyecto_id = %s WHERE id = %s"
    values = (entrada.dinero,entrada.fecha,entrada.proyecto_id,entrada.id)
    cursor.execute(query, values)
    conn.commit()
    return {"code": 200,"mensaje": "Se ha actualizado el registro"}