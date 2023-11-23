from fastapi import APIRouter, Request
from app.db.database import Database
from app.models import Cuenta

from app.utils.AdminToken import get_current_user


db = Database()
conn = db.conn
cursor = db.cursor
router = APIRouter()

@router.get('/user')
def user(req: Request):
    user = get_current_user(req.headers['Authorization'])
    return user

@router.post('/modificar')
def modificar(cuenta: Cuenta):
    query = "UPDATE cuentas SET nombre = %s, primer_apellido = %s, segundo_apellido = %s, email = %s, ingresos = %s WHERE id = %s"
    values = (cuenta.nombre,cuenta.primer_apellido,cuenta.segundo_apellido,cuenta.email,cuenta.ingresos,cuenta.id)
    cursor.execute(query, values)
    conn.commit()
    return {"code": 200,"mensaje": "Se ha actualizado el registro"}