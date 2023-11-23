from app.db.database import Database
from app.models import Cuenta
db = Database()
conn = db.conn
cursor = db.cursor

def CorreoValido(email:str):
        query = "SELECT COUNT(*) FROM cuentas WHERE email = %s"
        cursor.execute(query, [email])
        count = cursor.fetchone()
        return count[0] > 0
    
def ObtenerUsuario(email:str,password:str):
    query = "SELECT * FROM cuentas WHERE email = %s AND password = %s"
    cursor.execute(query, (email,password))
    diccionario = cursor.fetchone()
    if diccionario is not None and diccionario[0] is not None:
        return Cuenta.to_json(diccionario)
    else:
        return None
     


def ObtenerUsuarioSoloEmail(email:str):
    query = "SELECT * FROM cuentas WHERE email = %s"
    cursor.execute(query, [email])
    diccionario = cursor.fetchone()
    if diccionario is not None or diccionario[0] is not None:
        return Cuenta.to_json(diccionario)
    else: 
        return None
    
def ObtenerUsuarioSoloEmailDict(email:str):
    query = "SELECT * FROM cuentas WHERE email = %s"
    cursor.execute(query, [email])
    diccionario: dict = cursor.fetchone()
    if diccionario is not None:
        return diccionario
    else: 
        return None
    
def ObtenerUsuarioPorId(id: int):
    query = "SELECT * FROM cuentas WHERE id = %s"
    cursor.execute(query, [id])
    diccionario = cursor.fetchone()
    if diccionario is not None or diccionario[0] is not None:
        return Cuenta.to_json(diccionario)
    else: 
        return None
    
    