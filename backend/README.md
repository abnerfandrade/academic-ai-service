# Academic AI Service - Backend

Este é o repositório do backend do serviço **Academic AI Service**. Ele fornece a API, o processamento de documentos (RAG) e a lógica de inteligência artificial responsável por gerenciar sessões acadêmicas, gerar perguntas baseadas em conteúdo e avaliar respostas usando fluxos baseados em grafos.

## 🛠️ Stack Tecnológico

O projeto é construído sobre uma arquitetura moderna e robusta utilizando:

- **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
- **Banco de Dados Relacional**: [PostgreSQL](https://www.postgresql.org/) (com SQLAlchemy e Alembic para migrações)
- **Banco de Dados Vetorial**: [Qdrant](https://qdrant.tech/) (para recuperação e pipeline RAG)
- **Orquestração de IA e Agentes**: [LangChain](https://python.langchain.com/) e [LangGraph](https://langchain-ai.github.io/langgraph/)
- **Modelos de IA**: Integrações com OpenAI e Google GenAI (Gemini)
- **Processamento de Documentos**: PyMuPDF e MarkItDown
- **Qualidade de Código e Testes**: Pytest
- **Gerenciamento e Execução**: Docker, Docker Compose e Makefile

## 📂 Estrutura de Diretórios

A estrutura do projeto foi pensada para seguir boas práticas de separação de responsabilidades e arquitetura modular:

```text
backend/
├── alembic/                 # Migrações do banco de dados (Alembic)
├── src/
│   ├── agents/              # Lógica de agentes de IA e workflows LangGraph
│   │   └── leveling_graph/  # Fluxo de nivelamento acadêmico (LangGraph)
│   ├── core/                # Configurações gerais, logs, variáveis de ambiente
│   ├── db/                  # Conexão com o banco de dados e mapeamento de modelos
│   ├── middlewares/         # Middlewares FastAPI (ex: request_id)
│   ├── repositories/        # Padrão Repository para acesso ao banco (ex: user, document, session)
│   ├── routes/              # Endpoints da API (routers FastAPI)
│   └── services/            # Serviços de negócio (ex: pipeline RAG, Vector Store)
├── tests/                   # Testes unitários e de integração (Pytest)
├── .env.example             # Exemplo de variáveis de ambiente
├── docker-compose.yml       # Orquestração local dos containers (DB, Vector Store, API)
├── Dockerfile               # Imagem da aplicação
├── langgraph.json           # Configuração de deploy/ambiente do LangGraph Studio
├── Makefile                 # Comandos de atalho (dev, testes, infra)
└── requirements.txt         # Dependências do Python
```

## 🧠 Workflow LangGraph (Leveling Graph)

O coração da interação inteligente do sistema reside no fluxo do `LevelingGraph` (`src/agents/leveling_graph/`). Trata-se de uma máquina de estados gerida pelo LangGraph que avalia o conhecimento de um usuário através de um fluxo conversacional atualizado:

1. **`generate_questions`**: Injeta os pré-requisitos diretamente no estado inicial a partir da tabela `documents` e formula as questões para testar o usuário.
2. **`ask_question`**: Apresenta a questão ao usuário. O fluxo **pausa (interrupt)** aqui para aguardar a resposta.
3. **`evaluate_answer`**: Recebe a resposta do usuário e avalia seu nível de acerto.
4. **Roteamento Condicional (`route_loop`)**:
   - Se ainda há perguntas a serem feitas, retorna para `ask_question`.
   - Caso contrário, avança para `acknowledge_answers`.
5. **`acknowledge_answers`**: Confirma e dá feedback sobre as respostas. O fluxo **pausa (interrupt)** novamente aqui.
6. **`generate_report`**: Gera um relatório final consolidando a performance e o nivelamento do usuário.

*Nota: O estado do grafo é salvo de forma persistente no PostgreSQL através do `AsyncPostgresSaver`, permitindo sessões assíncronas duradouras com checkpointer.*

## 📚 Pipeline RAG (Retrieval-Augmented Generation)

O processamento inteligente de documentos na aplicação é conduzido pelo `RagPipeline`, orquestrando 4 etapas fundamentais para alimentar nossa IA com contexto de alta qualidade:

1. **Extração (`DocumentExtractor`)**: Lê o arquivo bruto submetido pelo usuário e extrai integralmente o texto.
2. **Chunking (`TokenChunker`)**: Divide o texto extraído de forma semântica em blocos menores (chunks) baseados em limites de tokens. Isso respeita a janela de contexto dos LLMs e maximiza a precisão da busca.
3. **Embedding e Armazenamento (`Embedder`)**: Converte os chunks de texto em vetores (embeddings) e os persiste no **Qdrant** para recuperação ultra-rápida baseada em similaridade.
4. **Extração de Objetivos (`ObjectiveExtractor`)**: Inspeciona o documento inteiro e, com auxílio da IA, mapeia os **pré-requisitos** e os **objetivos de aprendizado** principais do material. É este contexto enriquecido que alimenta o Grafo de Nivelamento.

## ⚙️ Como Configurar o Projeto

1. **Clone o repositório** e acesse a pasta `backend`.
2. **Crie e ative um ambiente virtual** (recomendado usar `venv`):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Instale as dependências**:
   ```bash
   make install
   ```
4. **Variáveis de Ambiente**:
   Crie uma cópia do arquivo de exemplo para as configurações locais.
   ```bash
   cp .env.example .env
   ```
   *Preencha o `.env` com as suas credenciais de banco de dados e as chaves de API necessárias (ex: `OPENAI_API_KEY`, `GEMINI_API_KEY`, etc).*

## 🚀 Como Rodar e Comandos Úteis

O repositório inclui um `Makefile` que simplifica as operações do dia a dia. Utilize os comandos abaixo:

### Infraestrutura Local
- **Subir Banco de Dados e Vector Store (Postgres e Qdrant)**:
  ```bash
  make infra-up
  ```
- **Derrubar Infraestrutura**:
  ```bash
  make infra-down
  ```

### Banco de Dados (Migrações)
- **Rodar as Migrações do Alembic**:
  ```bash
  make migrate
  ```
- **Rodar as Migrações dentro do Container da API** (requer que o container esteja rodando):
  ```bash
  make migrate-docker
  ```

### Backend (API)
- **Executar o Servidor de Desenvolvimento (Hot-reload)**:
  ```bash
  make dev
  ```
- **Rodar Testes Unitários**:
  ```bash
  make tests
  ```

### Orquestração de Grafos (LangGraph Studio)
- **Iniciar o LangGraph Studio**: Abre o ambiente de visualização e debug de workflows LangGraph locais.
  ```bash
  make smith
  ```

### Comandos Docker Globais
- **Subir toda a stack via Docker (incluindo API)**: `make up`
- **Derrubar toda a stack**: `make down`
- **Visualizar Logs da API**: `make logs`

## 🔗 Links Úteis da Aplicação

Com os serviços rodando localmente, os seguintes links estarão disponíveis:

- **Backend API (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Backend API (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Qdrant Dashboard (Vector Store)**: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)
- **LangGraph Studio UI**: Gerado no terminal ou abrindo no navegador ao rodar o comando `make smith`.
