import { useNavigate, useLocation } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { toast } from 'sonner'
import { usersApi } from '../../api/users'
import { useUserStore } from '../../stores/useUserStore'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Trash2, UserCheck, ArrowLeft } from 'lucide-react'
import type { UserResponse } from '../../types/user'

const schema = z.object({
  name: z.string().min(2, 'Nome obrigatório'),
  email: z.string().email('E-mail inválido'),
})
type FormData = z.infer<typeof schema>

export function UsuariosPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const queryClient = useQueryClient()
  const { user: activeUser, setUser } = useUserStore()
  const redirectTo = (location.state as any)?.redirectTo

  const { data: users, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: () => usersApi.list().then((r) => r.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: FormData) => usersApi.create(data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      toast.success('Usuário criado!')
      reset()
    },
    onError: () => toast.error('Erro ao criar usuário. E-mail já pode estar em uso.'),
  })

  const deleteMutation = useMutation({
    mutationFn: (userId: number) => usersApi.delete(userId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
    onError: () => toast.error('Erro ao deletar usuário.'),
  })

  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const handleSelect = (u: UserResponse) => {
    setUser(u)
    toast.success(`Usuário "${u.name}" selecionado.`)
    if (redirectTo) navigate(redirectTo)
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      <Button variant="ghost" onClick={() => navigate('/')}>
        <ArrowLeft size={16} className="mr-2" /> Voltar
      </Button>
      <h1 className="text-2xl font-bold">Usuários</h1>

      <form onSubmit={handleSubmit((d) => createMutation.mutate(d))} className="space-y-4 border rounded-lg p-4">
        <h2 className="font-semibold">Novo usuário</h2>
        <div>
          <Label>Nome</Label>
          <Input placeholder="João Silva" {...register('name')} />
          {errors.name && <p className="text-xs text-red-500 mt-1">{errors.name.message}</p>}
        </div>
        <div>
          <Label>E-mail</Label>
          <Input placeholder="joao@exemplo.com" {...register('email')} />
          {errors.email && <p className="text-xs text-red-500 mt-1">{errors.email.message}</p>}
        </div>
        <Button type="submit" disabled={createMutation.isPending}>
          {createMutation.isPending ? 'Criando...' : 'Criar usuário'}
        </Button>
      </form>

      <div className="space-y-3">
        <h2 className="font-semibold">Usuários cadastrados</h2>
        {isLoading
          ? <p className="text-sm text-muted-foreground">Carregando...</p>
          : users?.map((u) => (
            <div
              key={u.id}
              className={`border rounded-lg p-3 flex items-center justify-between ${activeUser?.id === u.id ? 'border-primary bg-primary/5' : ''}`}
            >
              <div>
                <p className="font-medium text-sm">{u.name}</p>
                <p className="text-xs text-muted-foreground">{u.email}</p>
              </div>
              <div className="flex gap-2">
                <Button size="sm" variant="outline" onClick={() => handleSelect(u)}>
                  <UserCheck size={14} className="mr-1" />
                  {activeUser?.id === u.id ? 'Selecionado' : 'Selecionar'}
                </Button>
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => deleteMutation.mutate(u.id)}
                  disabled={deleteMutation.isPending}
                >
                  <Trash2 size={14} className="text-red-500" />
                </Button>
              </div>
            </div>
          ))
        }
      </div>
    </div>
  )
}
