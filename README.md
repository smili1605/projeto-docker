# API FastAPI + PostgreSQL com Docker

Este projeto demonstra uma aplicação Dockerizada completa com FastAPI e PostgreSQL, incluindo configurações de segurança, redes e volumes.

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno para Python
- **PostgreSQL** - Banco de dados relacional
- **Docker** - Containerização da aplicação
- **Docker Compose** - Orquestração de multi-containers
- **SQLAlchemy** - ORM para Python
- **Uvicorn** - Servidor ASGI

## 📋 Pré-requisitos

- Docker
- Docker Compose

## 🏗️ Estrutura do Projeto
myapp/
├── app/
│ ├── init.py
│ ├── main.py # Aplicação FastAPI
│ ├── models.py # Modelos de dados
│ ├── database.py # Configuração do banco
│ └── schemas.py # Schemas Pydantic
├── docker-compose.yml # Configuração Docker Compose
├── Dockerfile # Build da imagem da aplicação
├── init.sql # Script de inicialização do PostgreSQL
├── requirements.txt # Dependências Python
├── .env # Variáveis de ambiente
└── README.md # Documentação

text

## 🛠️ Configuração e Execução

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd myapp

2. Configure as variáveis de ambiente
bash
cp .env.example .env
# Edite o arquivo .env com suas configurações

3. Execute os containers
bash
docker-compose up -d --build

4. Verifique se os containers estão rodando
bash
docker-compose ps

Acessando a Aplicação
API Documentation: http://localhost:8000/docs

API Base URL: http://localhost:8000

 Endpoints da API
Items
POST /items/ - Criar um novo item

GET /items/ - Listar todos os items

GET /items/{id} - Buscar item por ID

PUT /items/{id} - Atualizar item

DELETE /items/{id} - Deletar item

Exemplos de Uso
Criar um item
bash
curl -X POST "http://localhost:8000/items/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Notebook", "description": "Dell Inspiron", "price": 2500}'
Listar items
bash
curl "http://localhost:8000/items/"

 Banco de Dados
Serviço: PostgreSQL

Porta: 5432

Banco: app_db

Usuário da aplicação: app_user

Volume: postgres_data (persistência)

Comandos úteis para o banco
bash
# Acessar o PostgreSQL
docker-compose exec db psql -U app_user -d app_db

# Ver tabelas
\dt

# Sair
\q

 Comandos Docker Úteis
bash
# Ver logs da aplicação
docker-compose logs app

# Ver logs do banco
docker-compose logs db

# Parar containers
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Rebuildar imagens
docker-compose up -d --build

Segurança Implementada
Usuário específico para aplicação (não root)

Variáveis de ambiente para dados sensíveis

Rede isolada entre containers

Permissões mínimas necessárias no banco

Solução de Problemas
Se a aplicação não conectar ao banco
bash
docker-compose restart app
Se as tabelas não forem criadas
bash
docker-compose exec db psql -U postgres -d app_db -c "CREATE TABLE items (id SERIAL PRIMARY KEY, title VARCHAR(100) NOT NULL, description TEXT, price INTEGER NOT NULL);"

Variáveis de Ambiente
Edite o arquivo .env para configurar:

env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_DB=app_db

DB_USER=app_user
DB_PASSWORD=app_password
DB_HOST=db
DB_PORT=5432
DB_NAME=app_db

 Contribuição
Fork o projeto

Crie uma branch para sua feature

Commit suas mudanças

Push para a branch

Abra um Pull Request

 Licença
Este projeto está sob a licença MIT.

## 🗃️ AGORA OS ARQUIVOS SEM COMENTÁRIOS:

### 1. docker-compose.yml (SEM COMENTÁRIOS)

```yaml
services:
  app:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=${DB_HOST}
      - DB_PORT=${DB_PORT}
      - DB_NAME=${DB_NAME}
    depends_on:
      - db
    networks:
      - app-network
    volumes:
      - ./app:/app
    restart: unless-stopped
    command: >
      sh -c "sleep 15 &&
             uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    restart: unless-stopped
    ports:
      - "5432:5432"

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge