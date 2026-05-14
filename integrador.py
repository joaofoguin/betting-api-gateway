import jwt
import os
import datetime
from fastapi import FastAPI, HTTPException, Depends, Header
import requests
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs das APIs Destino
URL_LUTAS = "http://127.0.0.1:8001"
URL_LUTADORES = "https://api-lutadoressd.onrender.com/api" # API Externa

NOME_INTEGRADOR = "api_integrador"

SECRET_KEY = "sua_chave_secreta_super_segura" # Use uma variável de ambiente
ALGORITHM = "HS256"

# --- LÓGICA DE JWT ---

def criar_token(usuario: str):
    expiracao = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"sub": usuario, "exp": expiracao}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_jwt(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token ausente")
    try:
        # Formato esperado: "Bearer <TOKEN>"
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

def gerar_assinatura(rota: str):
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    mensagem = f"{NOME_INTEGRADOR}:{rota}"
    assinatura = private_key.sign(
        mensagem.encode("utf-8"),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return base64.b64encode(assinatura).decode("utf-8")

# --- ROTAS DE LUTAS (Sua API) ---
@app.get("/lutas/")
def get_lutas(usuario_logado = Depends(verificar_jwt)):
    rota = "/lutas/"
    headers = {"x-api-nome": NOME_INTEGRADOR, "x-assinatura": gerar_assinatura(rota)}
    r = requests.get(f"{URL_LUTAS}{rota}", headers=headers)
    return r.json()

@app.post("/lutas/")
def post_luta(dados: dict, usuario_logado = Depends(verificar_jwt)):
    rota = "/lutas/" # Certifique-se que a API destino tem a barra final se aqui tiver
    headers = {"x-api-nome": NOME_INTEGRADOR, "x-assinatura": gerar_assinatura(rota)}
    r = requests.post(f"{URL_LUTAS}{rota}", json=dados, headers=headers)
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Rota não encontrada na API de Lutas. Verifique a barra final /")
    return r.json()

@app.delete("/lutas/{id}")
def proxy_delete_luta(id: int, usuario_logado = Depends(verificar_jwt)):
    rota_interna = f"/lutas/{id}"
    assinatura = gerar_assinatura(rota_interna)
    headers = {"x-api-nome": "api_integrador", "x-assinatura": assinatura}
    
    try:
        r = requests.delete(f"{URL_LUTAS}{rota_interna}", headers=headers)
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar na API interna: {str(e)}")
    
# --- ROTAS DE LUTADORES (API Externa) ---
@app.get("/lutadores")
def get_lutadores(usuario_logado = Depends(verificar_jwt)):
    # Se a API externa não exigir assinatura, remova os headers abaixo
    rota = "/lutadores"
    r = requests.get(f"{URL_LUTADORES}{rota}") 
    return r.json()

@app.get("/lutadores/{id}")
def get_lutador_id(id: int, usuario_logado = Depends(verificar_jwt)):
    r = requests.get(f"{URL_LUTADORES}/lutadores/{id}")
    return r.json()

@app.delete("/lutadores/{id}")
def proxy_delete_lutador_externo(id: int, usuario_logado = Depends(verificar_jwt)):
    try:
        r = requests.delete(f"{URL_LUTADORES}/lutadores/{id}")
        if r.status_code == 204:
            return {"detail": "Lutador removido com sucesso da API externa"}
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Lutador não encontrado na API externa")
            
        return r.json()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com API externa: {str(e)}")

@app.post("/lutadores")
def proxy_post_lutadores(dados: dict, usuario_logado = Depends(verificar_jwt)):
    # Mapeia os dados recebidos do HTML para o formato esperado pela API externa
    payload = {
        "id": 0,
        "nome": dados.get("nome", ""),
        "categoria": dados.get("categoria", ""),
        "apelido": dados.get("apelido", ""),
        "arte": dados.get("arte", "")
    }
    
    try:
        r = requests.post(f"{URL_LUTADORES}/lutadores", json=payload)
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar na API externa: {str(e)}")
    
    import os

@app.post("/login")
def login(dados: dict):
    # O Python vai buscar no sistema operacional os valores de ADMIN_USER e ADMIN_PASS
    user_env = os.getenv("ADMIN_USER", "admin") # "admin" é o padrão caso não encontre
    pass_env = os.getenv("ADMIN_PASS", "admin")

    if dados.get("usuario") == user_env and dados.get("senha") == pass_env:
        token = criar_token(dados["usuario"])
        return {"token": token}
    
    raise HTTPException(status_code=401, detail="Credenciais incorretas")