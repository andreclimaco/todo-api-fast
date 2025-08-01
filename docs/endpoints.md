
# 📌 Endpoints da API

## 🔐 Autenticação

### POST `/register`
Cria um novo usuário e retorna um token JWT.

**Parâmetros:**
- `user`: Objeto com nome, email e senha.
- `db`: Sessão do banco de dados.

**Resposta:**
- Token JWT válido por 24 horas.

**Exemplo de Requisição**
```json
POST /register
{
  "nome": "João da Silva",
  "email": "joao@example.com",
  "senha": "123456"
}
```

**Exemplo de Resposta**
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}
```

---

### POST `/login`
Realiza login e retorna um token JWT.

**Parâmetros (form-data):**
- `username`: Email
- `password`: Senha

**Exemplo de Resposta**
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}
```

---

### GET `/me`
Retorna os dados do usuário autenticado.

**Cabeçalho necessário:**
- `Authorization: Bearer <token>`

**Resposta:**
```json
{
  "id": "UUID",
  "nome": "João da Silva",
  "email": "joao@example.com"
}
```

---

## ✅ Tarefas

### POST `/tasks/`
Cria uma nova tarefa.

**Parâmetros:**
- `tarefa`: Dados da tarefa.

**Resposta:**
- Tarefa criada com sucesso.

---

### GET `/tasks/`
Lista tarefas do usuário com filtros opcionais.

**Parâmetros opcionais:**
- `status`
- `prioridade`

---

### GET `/tasks/{tarefa_id}`
Recupera uma tarefa específica.

**Resposta:**
- Dados da tarefa.

---

### PUT `/tasks/{tarefa_id}`
Atualiza os dados de uma tarefa.

---

### DELETE `/tasks/{tarefa_id}`
Remove uma tarefa existente.

---

### POST `/tasks/{tarefa_id}/complete`
Marca uma tarefa como concluída.
