import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'

import { LandingPage } from './pages/LandingPage'
import { UploadPage } from './pages/professor/UploadPage'
import { DocumentsPage } from './pages/professor/DocumentsPage'
import { AulaListPage } from './pages/aluno/AulaListPage'
import { NivelamentoPage } from './pages/aluno/NivelamentoPage'
import { RelatorioPage } from './pages/aluno/RelatorioPage'
import { UsuariosPage } from './pages/usuarios/UsuariosPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 1000 * 30, retry: 1 },
  },
})

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/professor" element={<DocumentsPage />} />
          <Route path="/professor/upload" element={<UploadPage />} />
          <Route path="/professor/documentos" element={<DocumentsPage />} />
          <Route path="/aluno" element={<AulaListPage />} />
          <Route path="/aluno/nivelamento/:sessionId" element={<NivelamentoPage />} />
          <Route path="/aluno/nivelamento/:sessionId/relatorio" element={<RelatorioPage />} />
          <Route path="/usuarios" element={<UsuariosPage />} />
        </Routes>
      </BrowserRouter>
      <Toaster richColors position="top-right" />
    </QueryClientProvider>
  )
}
