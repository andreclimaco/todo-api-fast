# **Documento de Requisitos de Software (DRS)**

## Aplicação: TODO – Gerenciador de Tarefas

### Versão: 1.0

### Data: 01/08/2025

### Tecnologia principal: FastAPI (Python 3.11)

---

## **1. Introdução**

### 1.1 Propósito

Este documento descreve os requisitos funcionais e não funcionais do sistema TODO, uma aplicação de gerenciamento de tarefas baseada em API REST desenvolvida com FastAPI. O objetivo é permitir que usuários cadastrem, editem, visualizem, filtrem e excluam tarefas de forma eficiente e escalável.

### 1.2 Escopo do Sistema

O sistema TODO será um backend exposto via FastAPI, que possibilita integração com clientes web ou mobile. Os principais recursos incluem:

* Autenticação de usuários (JWT)
* CRUD de tarefas
* Marcação de prioridade e status
* Filtros e ordenação
* Integração com banco de dados relacional (PostgreSQL)
* Documentação automática com Swagger

---

## **2. Requisitos Funcionais**

### RF01 – Cadastro de Usuário

* O sistema deve permitir que um novo usuário se registre com nome, e-mail e senha.
* O e-mail deve ser único e validado.

### RF02 – Autenticação

* O sistema deve permitir login via e-mail e senha.
* Após autenticação, deve gerar e retornar um token JWT válido por 24h.
* O sistema deve proteger todas as rotas de tarefas, exceto o login e o cadastro.

### RF03 – Criação de Tarefa

* O usuário autenticado deve poder criar uma tarefa com:

  * Título (obrigatório)
  * Descrição (opcional)
  * Data de vencimento (opcional)
  * Prioridade: baixa, média, alta (padrão: média)
  * Status: pendente, em andamento, concluída (padrão: pendente)

### RF04 – Listagem de Tarefas

* O sistema deve permitir que o usuário veja todas as suas tarefas.
* Deve haver possibilidade de:

  * Filtrar por status e prioridade
  * Ordenar por data de criação ou vencimento

### RF05 – Atualização de Tarefa

* O usuário deve poder editar qualquer campo de uma tarefa de sua autoria.
* Campos não enviados devem permanecer inalterados.

### RF06 – Exclusão de Tarefa

* O usuário deve poder excluir tarefas individualmente.

### RF07 – Marcar como Concluída

* O sistema deve permitir alteração rápida de status para "concluída".

---

## **3. Requisitos Não Funcionais**

### RNF01 – Tecnologia e Frameworks

* O backend deve ser desenvolvido em **Python 3.11+** utilizando **FastAPI**.
* O banco de dados deve ser **PostgreSQL**.
* O ORM utilizado será o **SQLAlchemy 2.0 ou SQLModel**.

### RNF02 – Autenticação

* A autenticação será baseada em JWT.
* Tokens devem ser assinados com chave secreta e ter expiração definida.

### RNF03 – Documentação da API

* Toda a API deve ser documentada automaticamente com Swagger UI (via FastAPI).
* Também deverá estar disponível em `/docs` e `/redoc`.

### RNF04 – Deploy

* A aplicação será empacotada com Docker e orquestrada com Docker Compose.
* O deploy será feito em ambiente Linux Ubuntu 22.04.

### RNF05 – Testes

* O sistema deve possuir cobertura mínima de testes unitários de 80%.
* A framework de testes será `pytest`.

### RNF06 – Desempenho

* O sistema deve suportar no mínimo 100 requisições simultâneas sem degradação perceptível de desempenho (resposta < 1s).

---

## **4. Modelo de Dados (Entidades Principais)**

### Usuário

| Campo       | Tipo     | Regras                       |
| ----------- | -------- | ---------------------------- |
| id          | UUID     | Gerado automaticamente       |
| nome        | string   | Obrigatório                  |
| email       | string   | Único, obrigatório, validado |
| senha\_hash | string   | Criptografada com bcrypt     |
| criado\_em  | datetime | Auto gerado                  |

### Tarefa

| Campo            | Tipo     | Regras                                       |
| ---------------- | -------- | -------------------------------------------- |
| id               | UUID     | Gerado automaticamente                       |
| titulo           | string   | Obrigatório                                  |
| descricao        | text     | Opcional                                     |
| data\_vencimento | date     | Opcional                                     |
| prioridade       | enum     | \["baixa", "media", "alta"], padrão: "media" |
| status           | enum     | \["pendente", "em\_andamento", "concluida"]  |
| dono\_id         | UUID     | FK → Usuário                                 |
| criado\_em       | datetime | Auto gerado                                  |

---

## **5. API Endpoints (Resumo)**

| Método | Endpoint             | Descrição                    | Protegido |
| ------ | -------------------- | ---------------------------- | --------- |
| POST   | /auth/register       | Cadastro de usuário          | ❌         |
| POST   | /auth/login          | Login e geração de token     | ❌         |
| GET    | /tasks               | Listar tarefas               | ✅         |
| POST   | /tasks               | Criar tarefa                 | ✅         |
| GET    | /tasks/{id}          | Obter uma tarefa             | ✅         |
| PUT    | /tasks/{id}          | Atualizar tarefa             | ✅         |
| DELETE | /tasks/{id}          | Excluir tarefa               | ✅         |
| POST   | /tasks/{id}/complete | Marcar tarefa como concluída | ✅         |

---

## **6. Restrições**

* A senha deve conter no mínimo 8 caracteres.
* Um usuário só pode ver e manipular suas próprias tarefas.
* Todas as datas devem seguir o padrão ISO 8601 (YYYY-MM-DD).

---

## **7. Critérios de Aceitação**

* O sistema deve permitir login, CRUD de tarefas e listagem filtrável.
* Tarefas devem estar protegidas por autenticação.
* A documentação `/docs` deve refletir corretamente todos os endpoints.
* A aplicação deve passar todos os testes automatizados com cobertura ≥ 80%.

---

Se quiser, posso converter isso em `.docx`, `.pdf`, ou gerar os modelos de banco e os endpoints em código FastAPI. Deseja seguir para isso?
