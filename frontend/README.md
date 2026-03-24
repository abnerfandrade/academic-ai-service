# Academic AI Service - Frontend

Este é o repositório do frontend do serviço **Academic AI Service**. Ele fornece a interface gráfica simples para interagir com o backend, realizando uploads de documentos, acompanhando as sessões acadêmicas e respondendo aos fluxos de nivelamento inteligente.

## 🛠️ Stack Tecnológico

O projeto foi construído utilizando as melhores práticas e ferramentas do ecossistema React atual:

- **Framework Core**: [React 19](https://react.dev/) + [Vite](https://vitejs.dev/) (para build e dev server ultrarrápido)
- **Linguagem**: [TypeScript](https://www.typescriptlang.org/) (tipagem estática e segurança de código)
- **Estilização e UI**: 
  - [Tailwind CSS](https://tailwindcss.com/) (utilitários CSS)
  - [Radix UI](https://www.radix-ui.com/) (primitivas de UI acessíveis)
  - [Lucide React](https://lucide.dev/) (ícones)
- **Gerenciamento de Estado**: [Zustand](https://zustand-demo.pmnd.rs/) (estado global leve e rápido)
- **Data Fetching e API**: 
  - [React Query / TanStack Query](https://tanstack.com/query/latest) (cache, sincronização e estados de loading)
  - [Axios](https://axios-http.com/) (requisições HTTP)
- **Roteamento**: [React Router DOM](https://reactrouter.com/)
- **Formulários e Validação**: [React Hook Form](https://react-hook-form.com/) + [Zod](https://zod.dev/)
- **Renderização de Conteúdo**: [React Markdown](https://github.com/remarkjs/react-markdown) + Remark GFM (para exibir os relatórios e questões geradas pela IA)

## 📂 Estrutura de Diretórios

A arquitetura do projeto foca na modularidade e reuso de componentes:

```text
frontend/
├── dist/                  # Arquivos compilados para produção (gerado pelo build)
├── public/                # Assets estáticos globais (favicon, etc)
├── src/
│   ├── api/               # Configuração do Axios e chamadas para os endpoints do backend
│   ├── assets/            # Imagens, fontes e outros assets importados no código
│   ├── components/        # Componentes React reutilizáveis (UI base e componentes complexos)
│   ├── hooks/             # Custom hooks do React e integrações com React Query
│   ├── lib/               # Funções utilitárias (ex: classes de merge do Tailwind)
│   ├── pages/             # Componentes que representam as rotas/telas da aplicação
│   ├── stores/            # Lógica de estado global (Zustand)
│   ├── types/             # Definições e interfaces do TypeScript
│   ├── App.tsx            # Componente raiz da aplicação
│   └── main.tsx           # Ponto de entrada do React
├── .env                   # Variáveis de ambiente locais (ex: URL da API)
├── components.json        # Configurações de componentes base (ex: shadcn/ui)
├── eslint.config.js       # Configurações do linter
├── package.json           # Dependências e scripts do projeto
├── tailwind.config.js     # Configurações do tema e plugins do Tailwind CSS
├── tsconfig.json          # Configurações do compilador TypeScript
└── vite.config.ts         # Configurações do bundler Vite
```

## ⚙️ Como Configurar o Projeto

1. **Acesse a pasta do frontend**:
   ```bash
   cd frontend
   ```
2. **Instale as dependências** (O projeto utiliza `npm` como gerenciador de pacotes principal):
   ```bash
   npm install
   ```
3. **Configuração de Ambiente**:
   Se necessário, crie ou ajuste o arquivo `.env` na raiz da pasta `frontend` para apontar para a API correta. Por padrão, em desenvolvimento, o frontend espera se comunicar com a API do backend local.
   Exemplo de `.env`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

## 🚀 Como Rodar e Comandos Úteis

O projeto utiliza scripts do `npm` definidos no `package.json` para facilitar as tarefas:

### Servidor de Desenvolvimento
Inicia o Vite com hot-module replacement (HMR). O frontend ficará disponível localmente para acesso.
```bash
npm run dev
```

### Build para Produção
Gera a versão otimizada e minificada do projeto na pasta `dist/`. O TypeScript verifica os tipos antes de realizar o build.
```bash
npm run build
```

### Preview de Produção
Serve a pasta `dist/` localmente para que você possa testar o build final antes de realizar o deploy.
```bash
npm run preview
```

### Linter
Roda o ESLint para encontrar problemas de formatação e boas práticas no código.
```bash
npm run lint
```

### 🐳 Rodando com Docker
Você também pode rodar o frontend em um container localmente de forma rápida:

1. **Build e Execução**:
   Certifique-se de estar na raiz da pasta `frontend` e execute:
   ```bash
   docker compose up -d --build
   ```
2. **Acesso**:
   A aplicação estará disponível em: [http://localhost:5173](http://localhost:5173) (mapeada internamente para a porta 80 do Nginx).

3. **Derrubar o Container**:
   ```bash
   docker compose down
   ```

## 🔗 Links Úteis (Ambiente Local)

Lembre-se que para o frontend funcionar corretamente, o backend também deve estar em execução.

- **Aplicação Web (Frontend)**: [http://localhost:5173](http://localhost:5173) *(Porta padrão do Vite)*
- **Backend API (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
