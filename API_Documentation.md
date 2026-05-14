# 📄 Documentação da API - Gateway Integrador

Este serviço atua como um API Gateway. Todas as chamadas para os microsserviços de Lutas e Lutadores devem passar por aqui para que o usuário seja autenticado via JWT e a requisição seja internamente assinada (RSA) antes de ser repassada.

---

## 🔐 Autenticação (JWT)

A maioria das rotas exige um Token JWT válido. O token deve ser enviado no cabeçalho `Authorization` da seguinte forma:

`Authorization: Bearer <SEU_TOKEN_JWT>`

---

## 📌 Endpoints Expostos

### 👤 Autenticação
| Método | Rota | Proteção | Descrição |
| :--- | :--- | :--- | :--- |
| POST | `/login` | Nenhuma | Recebe `{"usuario": "...", "senha": "..."}` e retorna o token JWT. |

### ⚔️ Lutas (Redirecionamento para API Local)
| Método | Rota | Proteção | Descrição |
| :--- | :--- | :--- | :--- |
| GET | `/lutas/` | 🔐 JWT | Lista as lutas agendadas. |
| POST | `/lutas/` | 🔐 JWT | Agenda uma nova luta. |
| DELETE | `/lutas/{id}` | 🔐 JWT | Cancela uma luta existente. |

### 🥋 Lutadores (Redirecionamento para API Externa)
| Método | Rota | Proteção | Descrição |
| :--- | :--- | :--- | :--- |
| GET | `/lutadores` | 🔐 JWT | Lista todos os lutadores disponíveis. |
| GET | `/lutadores/{id}`| 🔐 JWT | Busca detalhes de um lutador específico. |
| POST | `/lutadores` | 🔐 JWT | Cadastra um novo lutador no serviço externo. |
| DELETE | `/lutadores/{id}`| 🔐 JWT | Remove um lutador do serviço externo. |

---

## 💡 Acesso Interativo (Swagger)

Como este Gateway é construído em FastAPI, você pode testar todas as rotas e ver os modelos JSON (Payloads) exatos acessando:
👉 `http://127.0.0.1:8000/docs`