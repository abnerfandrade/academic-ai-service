# Academic AI Service 🎓🤖

O **Academic AI Service** é uma plataforma educacional inteligente projetada para transformar a maneira como estudantes e pesquisadores interagem com materiais acadêmicos. Através de técnicas avançadas de **IA Generativa**, **RAG (Retrieval-Augmented Generation)** e **Grafos de Agentes**, a aplicação automatiza o processo de nivelamento, revisão e consolidação do conhecimento.

## 🌟 O que a plataforma atende?

A aplicação foi criada para resolver o desafio de processar grandes volumes de informação acadêmica e garantir que o aprendizado seja estruturado e mensurável. Ela atende:

- **Processamento de Documentos de Aula**: Extração inteligente de conteúdo de PDFs e materiais acadêmicos via pipeline RAG, com mapeamento de pré-requisitos e objetivos de aprendizado.
- **Nivelamento Acadêmico (Pré-aula)**: Avaliação dinâmica do conhecimento prévio através de diálogos guiados por IA, identificando gaps antes do módulo.
- **Consolidação de Aprendizado (Pós-aula)**: Validação da compreensão e aplicação prática do conteúdo após a aula, com relatórios de desempenho.

## 🏗️ Arquitetura do Ecossistema

O projeto é dividido em dois grandes módulos que trabalham em harmonia:

### 1. [Backend (FastAPI + LangGraph)](./backend/README.md)

O cérebro da aplicação. Gerencia processamento pesado, IA e persistência.

- **Grafos de Agentes (LangGraph)**: Dois fluxos conversacionais assíncronos com interrupções — Leveling Graph (pré-aula) e Consolidation Graph (pós-aula), ambos com persistência em PostgreSQL.
- **Pipeline RAG**: Extração de documentos, chunking semântico, embedding e armazenamento em **Qdrant**.
- **Stack**: FastAPI, PostgreSQL, Qdrant, LangChain/LangGraph, OpenAI/Gemini.

### 2. [Frontend (React 19 + Vite)](./frontend/README.md)

A interface do usuário, focada em simplicidade e fluidez.

- **Stack Moderno**: React 19, TypeScript, Vite (build ultrarrápido), Tailwind CSS e Radix UI.
- **Gerenciamento de Estado**: Zustand (estado global) e React Query (sincronização com API).
- **Componentes**: Upload de documentos, interface conversacional com agentes, exibição de relatórios com Markdown.

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
