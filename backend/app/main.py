from fastapi import FastAPI
from api import auth, user, pix, extrato, transactions
from models import models
from db.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(pix.router)
app.include_router(extrato.router)
app.include_router(transactions.router)