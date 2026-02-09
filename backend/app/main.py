from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api import auth, user, pix, extrato, transactions, contatos
from models import models
from db.database import engine
from schema.response import ErrorResponseSchema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = {err["loc"][-1]: "Campo obrigatório" for err in exc.errors()}
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Erro de validação nos campos",
            "data": errors,
            "error_code": "VALIDATION_ERROR"
        }
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    message = exc.detail if isinstance(exc.detail, str) else exc.detail.get("message", "Erro na requisição")
    error_code = "BAD_REQUEST" if isinstance(exc.detail, str) else exc.detail.get("error_code", "ERROR")

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseSchema(
            success=False,
            message=message,
            error_code=error_code
        ).model_dump()
    )

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(pix.router)
app.include_router(extrato.router)
app.include_router(transactions.router)
app.include_router(contatos.router)