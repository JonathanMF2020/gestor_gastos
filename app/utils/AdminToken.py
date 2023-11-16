from datetime import timedelta, datetime
from fastapi import Depends, HTTPException,status
from jose import JWTError, jwt
from app.models import Cuenta
from app.utils.config import oauth2_scheme
from app.utils.cuentas_util import ObtenerUsuarioPorId

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    newdata = Cuenta.to_dict(data)
    encoded_jwt = jwt.encode(newdata, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token_access(token: str):
    token_data = None
    token = token.replace('Bearer','')
    token = token.replace(' ','')
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        token_data = payload
    except JWTError as e:
        print(e)

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token_access(token)
    if user == None:
        raise HTTPException(status_code=500,detail="El token es incorrecto")
    else:
        return ObtenerUsuarioPorId(int(user['id']))   