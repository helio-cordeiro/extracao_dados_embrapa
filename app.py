
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from extraction import extrair_dados
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import datetime

# Inicializa o app FastAPI
app = FastAPI(title="Embrapa Data API")

# Configurações JWT
class Settings(BaseModel):
    authjwt_secret_key: str = "super-secret-key"

@AuthJWT.load_config
def get_config():
    return Settings()

# Define o modelo para o login
class UserLogin(BaseModel):
    username: str
    password: str

# Handler de exceção para JWT
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

# Rota de login para gerar token JWT
@app.post('/login')
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    if user.username != 'admin' or user.password != 'password':
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    # Gera o token JWT
    expires = datetime.timedelta(days=1)
    access_token = Authorize.create_access_token(subject=user.username, expires_time=expires)
    return {"access_token": access_token}

# Rota protegida que faz a extração dos dados
@app.get('/extrair')
def extrair(ano: str, opcao: str, subopcao: str, Authorize: AuthJWT = Depends()):
    # Verifica o token JWT
    Authorize.jwt_required()

    # Valida os parâmetros
    if not ano or not opcao or not subopcao:
        raise HTTPException(status_code=400, detail="Parâmetros insuficientes: ano, opcao, subopcao são obrigatórios")

    # Chama a função para extrair os dados
    dados = extrair_dados(ano, opcao, subopcao)

    # Retorna os dados ou um erro se a extração falhar
    if dados:
        return dados
    else:
        raise HTTPException(status_code=500, detail="Não foi possível extrair os dados ou dados não encontrados")

# Inicia o servidor FastAPI (use `uvicorn` para executar)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)