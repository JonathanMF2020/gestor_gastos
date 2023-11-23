from typing import Annotated
from fastapi import APIRouter, HTTPException
from app.models import Credenciales, Cuenta
from app.db.database import Database
from app.utils.AdminToken import create_access_token
from app.utils.hash import encrypt
from app.utils.cuentas_util import CorreoValido, ObtenerUsuarioSoloEmail, ObtenerUsuarioSoloEmailDict

db = Database()
conn = db.conn
cursor = db.cursor
router = APIRouter()

def fake_hash_password(password: str):
    return "fakehashed" + password


@router.post('/login')
async def login(input: Credenciales):
    
    if not input:
        raise HTTPException(status_code=500, detail="Incorrect login")
    user: dict = ObtenerUsuarioSoloEmailDict(input.email)
    if(user == None):
        raise HTTPException(status_code=500, detail="Email o password incorrecto")
    #hashed_password = fake_hash_password(form_data.password)
    userObject = Cuenta.to_json(user)
    hashed = encrypt(input.password)
    access = create_access_token(user)
    if hashed == userObject.password:
        userObject.access_token = access
        userObject.status_code = 200
        return userObject
    else:
        return HTTPException(status_code=500,detail="La contraseña no coincide")
    #return {"access_token": user.nombre, "token_type": "bearer","hashed": hashed_password}
    


@router.post("/register")
def register(cuenta: Cuenta):
    valido = CorreoValido(cuenta.email)
    if valido is True:
         raise HTTPException(status_code=500, detail="Ya existe ese email")
    newpassword = encrypt(cuenta.password)
    cuenta.password = newpassword
    query = "INSERT INTO cuentas (nombre, primer_apellido, segundo_apellido, email, password) VALUES (%s, %s, %s, %s, %s)"
    values = (cuenta.nombre,cuenta.primer_apellido,cuenta.segundo_apellido,cuenta.email,cuenta.password)
    cursor.execute(query, values)
    conn.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    last_insert_id = cursor.fetchone()[0]
    cuenta.id = last_insert_id
    
    return cuenta