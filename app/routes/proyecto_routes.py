from datetime import datetime,timedelta
from fastapi import APIRouter, HTTPException, Request
from app.db.database import Database

from app.models import Proyecto
from app.utils.AdminToken import get_current_user

db = Database()
conn = db.conn
cursor = db.cursor
router = APIRouter()

@router.get('/simulador/')
def simulador(id: int, req: Request):
    user = get_current_user(req.headers['Authorization'])
    query = "SELECT * FROM proyectos WHERE cuenta_id = %s AND id = %s"
    cursor.execute(query, [user.id,id])
    diccionarios = cursor.fetchone()
    proyecto = Proyecto.to_json(diccionarios,user)
    fecha_actual = proyecto.inicio
    retorno = proyecto.limite - fecha_actual 
    meses = retorno.days/30
    meses = proyecto.monto/user.ingresos
    fecha_con_meses_sumados = fecha_actual + timedelta(days=int(retorno.days))
    total = 0
    matriz = []
    json = {}
    fechaabono = fecha_actual
    for i in range(int(meses)):
        total += user.ingresos
        fechaabono = fechaabono + timedelta(days=int(30))
        if(fechaabono > proyecto.limite):
            enrango = False
        else:
            enrango = True
        pago = {"mes": i,"fecha": fechaabono, "abono": user.ingresos,"total": total,'resta': proyecto.monto-total,'meta': proyecto.monto,"enrango": enrango}
        matriz.append(pago)
    
    json['analisis'] = {"inicio": proyecto.inicio,"fin_estimado": fecha_con_meses_sumados,"fin_real": fechaabono,"meses": meses,"total": total}
    json['matriz'] = matriz
    
    return json
    
@router.post('/registrar')
def registrar(proyecto: Proyecto,req: Request):
    
    user = get_current_user(req.headers['Authorization'])
    proyecto.cuenta_id = user.id
    proyecto.cuenta = user
    query = "INSERT INTO proyectos (nombre, descripcion, monto, cuenta_id, estatus,inicio, limite) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (proyecto.nombre,proyecto.descripcion,proyecto.monto,proyecto.cuenta_id,1,proyecto.inicio,proyecto.limite)
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

@router.post('/terminar')
def obtenertodo(id: int):
    query = "UPDATE proyectos SET estatus = 0 WHERE id = %s"
    cursor.execute(query, [id])
    conn.commit()
    return {"code": 200,"mensaje": "Se ha actualizado el registro"}

@router.post('/activar')
def obtenertodo(id: int):
    query = "UPDATE proyectos SET estatus = 1 WHERE id = %s"
    cursor.execute(query, [id])
    conn.commit()
    return {"code": 200,"mensaje": "Se ha actualizado el registro"}

@router.get('/obtener/')
def obtenertodo(id: int,req: Request):
    
    user = get_current_user(req.headers['Authorization'])
    query = "SELECT * FROM proyectos WHERE cuenta_id = %s AND id = %s"
    cursor.execute(query, [user.id,id])
    diccionarios = cursor.fetchone()
    print(diccionarios)
    if diccionarios is not None:
        query2 = "SELECT SUM(e.dinero) AS total FROM entrada AS e INNER JOIN proyectos AS p ON(e.proyecto_id = p.id) WHERE p.id = %s"
        cursor.execute(query2, [id])
        resultado = cursor.fetchone()[0]
        retornado = {}
        proyecto = Proyecto.to_json(diccionarios,user)
        if(resultado != None):
            resultado = float(resultado)
            restante = proyecto.monto - resultado
            retornado['total'] = resultado   
            if(restante <= 0):
                retornado['restante'] = 0
                retornado['estatus'] = "Concluido"
            else:
                retornado['restante'] = restante
                retornado['estatus'] = "En proceso"
            retornado['proyecto'] = proyecto
            return retornado
        else: return HTTPException(status_code=500,detail="No se encontro dinero acreditado a este proyecto")
    else: 
        return HTTPException(status_code=500,detail="No existe el registro")
    

