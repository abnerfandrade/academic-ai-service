import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { toast } from 'sonner'
import { documentsApi } from '../../api/documents'
import { useState } from 'react'

const schema = z.object({
  class_name: z.string().min(3, 'Nome da aula deve ter ao menos 3 caracteres'),
  file: z
    .instanceof(FileList)
    .refine((fl) => fl.length === 1, 'Selecione um arquivo')
    .refine((fl) => fl[0]?.type === 'application/pdf', 'Apenas arquivos PDF são aceitos'),
})

type FormData = z.infer<typeof schema>

interface Props {
  onSuccess: (documentId: number) => void
}

export function UploadForm({ onSuccess }: Props) {
  const [isLoading, setIsLoading] = useState(false)
  const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    setIsLoading(true)
    try {
      const res = await documentsApi.upload(data.file[0], data.class_name)
      toast.success(`Aula "${res.data.class_name}" enviada! Processando...`)
      reset()
      onSuccess(res.data.id)
    } catch (err: any) {
      const status = err?.response?.status
      if (status === 409) toast.error('Esse arquivo já foi enviado anteriormente.')
      else if (status === 413) toast.error('Arquivo muito grande. Máximo: 10MB.')
      else if (status === 422) toast.error('Formato não suportado. Envie um PDF.')
      else toast.error('Erro ao enviar. Tente novamente.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="class_name">Nome da aula</Label>
        <Input id="class_name" placeholder="Ex: Cálculo I — Aula 1" {...register('class_name')} />
        {errors.class_name && <p className="text-sm text-red-500 mt-1">{errors.class_name.message}</p>}
      </div>
      <div>
        <Label htmlFor="file">Arquivo PDF</Label>
        <Input id="file" type="file" accept=".pdf" {...register('file')} />
        {errors.file && <p className="text-sm text-red-500 mt-1">{errors.file.message as string}</p>}
      </div>
      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? 'Enviando...' : 'Enviar aula'}
      </Button>
    </form>
  )
}
