````markdown id="e7gk3p"
# 🛡️ API Gateway & Cliente Web - Apostas em Lutas

Este repositório atua como o **API Gateway** e a interface de usuário (**Frontend**) para o ecossistema distribuído de agendamento de lutas. Desenvolvido como parte da disciplina de Sistemas Distribuídos, este serviço é a única porta de entrada para os usuários, orquestrando a comunicação com os microsserviços de backend de forma isolada e segura.

---

# 🏗️ Arquitetura e Fluxo de Segurança

Este serviço implementa dois níveis distintos de segurança (**Segurança em Camadas**).

---

## 🔐 1. Autenticação de Usuário (Frontend ➡️ Gateway)

A autenticação do usuário é realizada utilizando:

- **JWT (JSON Web Tokens)**

### Fluxo

1. O usuário realiza login via interface Web (`index.html`).
2. O Gateway valida as credenciais.
3. Um token JWT com expiração de **1 hora** é gerado.
4. O token é armazenado no:

```javascript
localStorage
````

5. As próximas requisições utilizam o token para acessar rotas protegidas.

---

## 🛡️ 2. Autenticação Machine-to-Machine (Gateway ➡️ Backend)

A comunicação entre o Gateway e o microsserviço de lutas utiliza:

* **Criptografia Assimétrica RSA**
* Padding **PSS**
* Hash **SHA256**

### Fluxo de Segurança

1. O Gateway intercepta a requisição do usuário.
2. Os dados são assinados utilizando a **Chave Privada RSA**.
3. A assinatura é enviada via cabeçalho HTTP:

```http
x-assinatura
```

4. O microsserviço valida a assinatura utilizando a **Chave Pública**.

Isso garante:

* Autenticidade
* Integridade
* Comunicação segura entre serviços
* Proteção contra falsificação de requisições

---

# 📡 Integrações (Microsserviços)

O Gateway atua como proxy/intermediário para duas APIs distintas.

---

## 🥊 API de Lutas (Microsserviço Interno)

```bash
http://127.0.0.1:8001
```

Características:

* Acesso restrito
* Comunicação protegida por RSA
* Persistência de dados das lutas

---

## 🧑‍🤝‍🧑 API de Lutadores (Microsserviço Externo)

```bash
https://api-lutadoressd.onrender.com/api
```

Responsável por:

* Consulta de atletas
* Cadastro de lutadores
* Validação de IDs

---

# 🚀 Como Executar Localmente

## 1️⃣ Pré-requisitos

Certifique-se de possuir:

* Python 3.x instalado
* Git instalado

---

## 2️⃣ Clonar o Repositório

```bash
git clone https://github.com/joaofoguin/betting-api-gateway
cd betting-api-gateway
```

---

## 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

---

# 🔑 Geração de Chaves Criptográficas (Primeiro Uso)

Antes de iniciar o servidor, gere o par de chaves RSA executando:

```bash
python chaves.py
```

Serão criados os arquivos:

```bash
private_key.pem
public_key.pem
```

## 📌 Importante

* `private_key.pem`

  * Deve permanecer somente neste repositório.
  * Nunca deve ser compartilhada.

* `public_key.pem`

  * Deve ser copiada para o repositório da API de Lutas.
  * Será utilizada para validar assinaturas.

---

# 🌎 Variáveis de Ambiente (Login)

O sistema busca as credenciais administrativas através de variáveis de ambiente.

Caso não existam, o padrão utilizado será:

| Campo   | Valor   |
| ------- | ------- |
| Usuário | `admin` |
| Senha   | `admin` |

---

# ▶️ Iniciando o Servidor

Execute:

```bash
uvicorn integrador:app --port 8000 --reload
```

O Gateway estará disponível em:

👉 `http://127.0.0.1:8000`

---

# 💻 Acessando a Interface Web

Abra diretamente o arquivo:

```bash
index.html
```

ou utilize ferramentas como:

* Live Server (VS Code)
* Python HTTP Server
* Nginx/Apache local

---

# 📁 Estrutura do Projeto

```bash
betting-api-gateway/
├── integrador.py        # Servidor principal FastAPI e rotas de Proxy
├── chaves.py            # Script utilitário para geração RSA
├── cliente_teste.py     # Testes locais de assinatura criptográfica
├── index.html           # Interface do usuário
├── script.js            # Lógica Frontend e gerenciamento JWT
├── style.css            # Estilização da interface
└── requirements.txt     # Dependências do projeto
```

---

# 🧠 Conceitos de Sistemas Distribuídos Aplicados

Este projeto implementa diversos conceitos importantes da disciplina:

* API Gateway
* Microsserviços
* Comunicação distribuída
* Segurança em camadas
* JWT Authentication
* Criptografia RSA
* Assinatura digital
* Proxy reverso
* Arquitetura cliente-servidor
* Integração síncrona entre APIs
* Autenticação M2M
* Segurança Zero Trust

---

# 👨‍💻 Autores

* João Pedro Silva da Rosa Lima
* Armando Alves de Oliveira Braga
* Sophia Ishii Dognani

```
```
