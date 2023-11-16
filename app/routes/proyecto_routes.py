from fastapi import APIRouter, Request
from app.db.database import Database

from app.models import Proyecto
from app.utils.AdminToken import get_current_user

db = Database()
conn = db.conn
cursor = db.cursor
router = APIRouter()

@router.post('/registrar')
def registrar(proyecto: Proyecto,req: Request):
    
    user = get_current_user(req.headers['Authorization'])
    proyecto.cuenta_id = user.id
    proyecto.cuenta = user
    query = "INSERT INTO proyectos (nombre, descripcion, monto, cuenta_id) VALUES (%s, %s, %s, %s)"
    values = (proyecto.nombre,proyecto.descripcion,proyecto.monto,proyecto.cuenta_id)
    cursor.execute(query, values)
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    last_insert_id = cursor.fetchone()[0]
    proyecto.id = last_insert_id
    return proyecto



@router.get('/obtenertodo')
def obtenertodo(req: Request):
    
    user = get_current_user(req.headers['Authorization'])
    query = "SELECT * FROM proyectos WHERE cuenta_id = %s"
    cursor.execute(query, [user.id])
    diccionarios = cursor.fetchall()
    arreglo = []
    for diccionario in diccionarios:
        arreglo.append(Proyecto.to_json(diccionario,user))
    return arreglo