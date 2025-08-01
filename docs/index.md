
# Documentação do Projeto TODO API

Esta aplicação é uma API RESTful construída com **FastAPI**, utilizando autenticação JWT, PostgreSQL, Alembic para migração de banco de dados e Docker para orquestração.

---

## 📦 Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **Alembic**
- **PostgreSQL**
- **Docker & Docker Compose**
- **JWT (Autenticação)**

---

## 📁 Estrutura de Diretórios

```
TODO/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── *.py  ← Scripts de migração
├── app/
│   ├── main.py  ← Ponto de entrada da API
│   ├── database.py  ← Conexão com o banco
│   ├── models.py  ← Modelos SQLAlchemy
│   ├── schemas.py  ← Schemas Pydantic
│   ├── security.py  ← Autenticação e criptografia
│   ├── repositories.py  ← Funções de acesso ao banco
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py  ← Endpoints de autenticação
│       └── tasks.py  ← Endpoints de tarefas
```

---

## ⚙️ Como Configurar o Ambiente

### 1. Pré-requisitos

- Docker instalado: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Docker Compose

### 2. Clonar o Projeto

Você pode descompactar o projeto ou clonar de um repositório (caso esteja hospedado no Git).

### 3. Variáveis de Ambiente

A aplicação já usa valores padrão no código:

- `DATABASE_URL`: `"postgresql://postgres:postgres@db:5432/tododb"`
- `SECRET_KEY`: `"chave-secreta-super-segura"`

Você pode usar variáveis de ambiente reais em produção.

---

## ▶️ Como Executar a Aplicação

### Com Docker (recomendado)

```bash
docker-compose up --build
```

Isso irá:
- Criar os containers do PostgreSQL e da API FastAPI.
- Subir a aplicação em `http://localhost:8000`.

---

### Testar API via Swagger

Acesse:

```
http://localhost:8000/docs
```

---

## 🧪 Rotas Disponíveis

### Autenticação (`/auth`)

| Método | Rota          | Descrição                  |
|--------|---------------|----------------------------|
| POST   | `/register`   | Registrar novo usuário     |
| POST   | `/login`      | Login e geração de token   |
| GET    | `/me`         | Dados do usuário logado    |

### Tarefas (`/tasks`)

| Método | Rota              | Descrição                          |
|--------|-------------------|------------------------------------|
| POST   | `/tasks/`         | Criar nova tarefa                  |
| GET    | `/tasks/`         | Listar tarefas do usuário          |
| GET    | `/tasks/{id}`     | Obter tarefa por ID                |
| PUT    | `/tasks/{id}`     | Atualizar tarefa                   |
| DELETE | `/tasks/{id}`     | Excluir tarefa                     |
| POST   | `/tasks/{id}/complete` | Marcar tarefa como concluída  |

---

## 🗃️ Migrações com Alembic

### Criar nova migração:

```bash
docker-compose exec api alembic revision --autogenerate -m "mensagem"
```

### Aplicar migrações:

```bash
docker-compose exec api alembic upgrade head
```

---

## 👤 Autores

- Projeto genérico para fins didáticos

---

## 🛡️ Segurança

- Senhas são armazenadas com hash `bcrypt`.
- Autenticação com tokens JWT válidos por 24 horas.

---

## ✅ Observações

- A API está pronta para uso com clientes front-end ou ferramentas como Postman, Insomnia, etc.
- Ideal para estudo de autenticação, APIs REST e Docker.
