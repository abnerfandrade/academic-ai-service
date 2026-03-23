import { useNavigate } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { GraduationCap, BookOpen, Users } from 'lucide-react'

export function LandingPage() {
  const navigate = useNavigate()
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-8 p-6 bg-background">
      <div className="text-center">
        <h1 className="text-3xl font-bold">Academic AI</h1>
        <p className="text-muted-foreground mt-1">Nivelamento inteligente pré-aula</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-xl">
        <Card
          className="cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => navigate('/professor')}
        >
          <CardHeader>
            <GraduationCap size={32} className="text-blue-500" />
            <CardTitle>Sou Professor</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">Envie o PDF da sua aula para preparar o nivelamento.</p>
          </CardContent>
        </Card>
        <Card
          className="cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => navigate('/aluno')}
        >
          <CardHeader>
            <BookOpen size={32} className="text-green-500" />
            <CardTitle>Sou Aluno</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">Responda o questionário antes da aula e veja seu relatório.</p>
          </CardContent>
        </Card>
      </div>
      <Button variant="ghost" size="sm" onClick={() => navigate('/usuarios')}>
        <Users size={16} className="mr-2" /> Gerenciar usuários
      </Button>
    </div>
  )
}
