from typing import Union

from fastapi import FastAPI, Depends
from app.routes import auth_routes
from app.routes import user_routes
from app.routes import proyecto_routes
from app.db.database import Database
from app.utils.config import oauth2_scheme

app = FastAPI()
db = Database()
conn = db.conn

PROTECTED = [Depends(oauth2_scheme)]
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(proyecto_routes.router, prefix="/proyecto",dependencies=PROTECTED)
app.include_router(user_routes.router, prefix="/user",dependencies=PROTECTED)

@app.on_event("shutdown")
def shutdown_db():
    conn.close()




