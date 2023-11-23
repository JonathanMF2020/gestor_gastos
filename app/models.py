from datetime import datetime
from pydantic import BaseModel

class Cuenta(BaseModel):
    id:int = None
    nombre:str
    primer_apellido:str
    segundo_apellido:str
    email:str
    password:str = None
    ingresos:float
    access_token:str = None
    status_code:int= 200
    
    
    def to_dict(cuenta: tuple):
        return {"id": cuenta[0],"nombre": cuenta[1],"primer_apellido": cuenta[2],"segundo_apellido": cuenta[3],"password": cuenta[4],"ingresos": cuenta[5]}

    def to_json(dicti: dict):
        return Cuenta(id=dicti[0],nombre=dicti[1],primer_apellido=dicti[2],segundo_apellido=dicti[3],email=dicti[4],password=dicti[5],ingresos=dicti[6])

    
    
class Credenciales(BaseModel):
    email: str
    password: str
    
    
class Proyecto(BaseModel):
    id:int = None
    nombre:str
    descripcion:str
    monto:float
    cuenta_id: int = None
    cuenta: Cuenta = None
    estatus: bool
    limite: datetime = None
    inicio: datetime = None
    
    def to_json(dicti: dict,cuenta:Cuenta = None):
        return Proyecto(id=dicti[0],nombre=dicti[1],descripcion=dicti[2],monto=dicti[3],
                        cuenta_id=dicti[4],estatus=dicti[5],limite=dicti[6],inicio=dicti[7],cuenta=cuenta)
        
    
class Entrada(BaseModel):
    id: int = None
    dinero:float
    fecha:datetime
    proyecto_id: int
    proyecto: Proyecto = None