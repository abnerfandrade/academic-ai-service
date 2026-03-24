# Academic AI Service 🎓🤖

O **Academic AI Service** é uma plataforma educacional inteligente projetada para transformar a maneira como estudantes e pesquisadores interagem com materiais acadêmicos. Através de técnicas avançadas de **IA Generativa**, **RAG (Retrieval-Augmented Generation)** e **Grafos de Agentes**, a aplicação automatiza o processo de nivelamento, revisão e consolidação do conhecimento.

## 🌟 O que a plataforma atende?

A aplicação foi criada para resolver o desafio de processar grandes volumes de informação acadêmica e garantir que o aprendizado seja estruturado e mensurável. Ela atende:

- **Processamento de Documentos de Aula**: Extração inteligente de conteúdo de PDFs e materiais acadêmicos para alimentar a base de conhecimento.
- **Nivelamento Automatizado**: Avaliação dinâmica do conhecimento através de diálogos guiados por IA, que culminam na identificação de gaps e auxiliam no nivelamento do aluno antes de iniciar uma aula.

## 🏗️ Arquitetura do Ecossistema

O projeto é dividido em dois grandes módulos que trabalham em harmonia:

### 1. [Backend (FastAPI + LangGraph)](./backend/README.md)
O cérebro da aplicação. Gerencia o processamento pesado e a lógica de IA.
- **Pipeline RAG**: Utiliza o **Qdrant** (Vector Database) para armazenar e recuperar fragmentos de documentos com alta precisão semântica.
- **LangGraph**: Orquestra o fluxo de "Nivelamento Acadêmico" como uma máquina de estados, permitindo interações humanas com memória e interrupções.
- **PostgreSQL**: Garante a persistência de usuários, sessões e o estado dos grafos de IA.

### 2. [Frontend (React + Vite)](./frontend/README.md)
A interface do usuário, focada em simplicidade e fluidez.
- **Interface Responsiva**: Desenvolvida com **Tailwind CSS** e **Radix UI**.
- **Gerenciamento de Estado**: Utiliza **Zustand** e **React Query** para uma experiência de usuário sem engasgos.
- **Markdown Rendering**: Exibe as interações com a IA de forma rica e formatada.

## 🚀 Como começar rapidamente

Para rodar o projeto completo em sua máquina, você deve seguir as instruções específicas de cada diretório:

1. **Infraestrutura**: Certifique-se de ter o **Docker** instalado para subir o Banco de Dados e o Vector Store.
2. **Backend**: Siga o [Guia do Backend](./backend/README.md) para configurar o ambiente Python e as chaves de API (OpenAI/Gemini).
3. **Frontend**: Siga o [Guia do Frontend](./frontend/README.md) para instalar as dependências via NPM e rodar a interface.

## 🔗 Atalhos de Acesso (Local)

Após configurar e rodar os serviços, utilize os links abaixo:

- 🖥️ **Web App**: [http://localhost:5173](http://localhost:5173)
- ⚙️ **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📊 **Vector Database Dashboard**: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)
