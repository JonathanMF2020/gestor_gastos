from pydantic import BaseModel

class Cuenta(BaseModel):
    id:int = None
    nombre:str
    primer_apellido:str
    segundo_apellido:str
    email:str
    password:str
    
    
    def to_dict(cuenta: tuple):
        return {"id": cuenta[0],"nombre": cuenta[1],"primer_apellido": cuenta[2],"segundo_apellido": cuenta[3],"password": cuenta[4]}

    def to_json(dicti: dict):
        return Cuenta(id=dicti[0],nombre=dicti[1],primer_apellido=dicti[2],segundo_apellido=dicti[3],email=dicti[4],password=dicti[5])

    
    
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
    
    def to_json(dicti: dict,cuenta:Cuenta):
        return Proyecto(id=dicti[0],nombre=dicti[1],descripcion=dicti[2],monto=dicti[3],
                        cuenta_id=dicti[4],cuenta=cuenta)
    