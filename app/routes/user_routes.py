from fastapi import APIRouter, Request
from app.models import Cuenta

from app.utils.AdminToken import get_current_user


router = APIRouter()

@router.get('/user')
def user(req: Request):
    user = get_current_user(req.headers['Authorization'])
    return user