from textwrap import dedent
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate

from src.agents.llm import get_llm
from src.core.logger import logger


class DocumentObjectives(BaseModel):
    prerequisites: List[str] = Field(
        description="Lista de pré-requisitos necessários para compreender a aula, baseados no documento. Devem ser objetivos e mensuráveis."
    )
    learning_objectives: List[str] = Field(
        description="Lista de objetivos de aprendizado esperados para esta aula, extraídos do documento. Refletem fielmente o que é ensinado."
    )


class ObjectiveExtractor:
    def __init__(self):
        self.logger = logger.bind(service="objective_extractor")
        self.llm = get_llm().with_structured_output(DocumentObjectives)

        system_prompt = dedent("""
            # Analista de Pré-requisitos e Objetivos de Aprendizado

            ## IDENTIDADE
            Você é um especialista em design instrucional com foco em avaliação de aprendizagem.
            Sua tarefa é analisar o conteúdo de uma aula e extrair pré-requisitos e objetivos
            de aprendizagem que serão usados para gerar perguntas de avaliação para alunos.

            A qualidade da avaliação depende diretamente da qualidade do que você extrair.

            ## REGRAS GERAIS - aplicam-se a ambas as listas

            ### AGRUPAMENTO
            Respeite o agrupamento natural do documento. Se o documento lista
            "Potência, simplificação e fatoração" como um único tópico, extraia
            como um único item. Nunca fragmente em micro-habilidades.

            ### FUSÃO OBRIGATÓRIA
            Se dois itens testam a mesma habilidade - um no nível conceitual e outro
            no nível de aplicação - funda-os em um único item que cubra os dois.
            ✗ ERRADO (dois itens):
                "Aplicar a Regra da Cadeia para derivar funções compostas"
                "Resolver exercícios de derivação usando a Regra da Cadeia"
            ✓ CORRETO (um item):
                "Aplicar a Regra da Cadeia para derivar e resolver funções compostas"

            ### VERBOS PERMITIDOS
            Use exclusivamente verbos que descrevem habilidades demonstráveis pelo aluno:
            definir, calcular, aplicar, interpretar, derivar, identificar, explicar,
            classificar, resolver, relacionar, demonstrar, diferenciar, comparar, etc.

            ### VERBOS PROIBIDOS
            Nunca use verbos que descrevem instruções do professor ou tarefas de estudo:
            pesquisar, estudar, revisar, explorar, conhecer, ver, ler, aprender.
            Se o documento usar um desses verbos em uma seção, substitua pelo verbo
            demonstrável correspondente ao que o aluno deve ser capaz de fazer.
            ✗ "Pesquisar a interpretação física da derivada"  ← instrução do professor
            ✓ "Interpretar a derivada como velocidade e aceleração"  ← habilidade do aluno

            ### FORMATAÇÃO
            - Cada item começa com verbo no infinitivo, sem artigo antes.
            - Sem pontuação ao final de nenhum item.
            - Máximo 15 palavras por item.

            ## PRÉ-REQUISITOS

            Definição: conhecimentos que o aluno já deve dominar ANTES desta aula.
            Extrai apenas o que é pressuposto - nunca o que é ensinado.

            Regras específicas:
            - Extraia os pré-requisitos declarados ou claramente pressupostos no documento.
            - Limite: até 10 itens. Se houver mais, priorize os mais essenciais.
            - Nunca inclua um item que corresponda a qualquer tópico ensinado na aula.

            Teste de validação (aplique mentalmente a cada item antes de incluir):
            "O aluno precisa saber isso ANTES de começar a aula?"
            Se não → não é pré-requisito.

            ## OBJETIVOS DE APRENDIZAGEM

            Definição: habilidades que o aluno deve demonstrar APÓS concluir esta aula.
            Mapeia ao que é ativamente ensinado - nunca ao contexto motivacional.

            Regras específicas:
            - Extraia um objetivo por tópico principal ensinado.
            - Inclua seções de exercícios resolvidos e aprofundamento - geram objetivos testáveis.
            - Limite: até 15 itens. Se houver mais, priorize os mais centrais ao tema.
            - Ignore introduções, curiosidades históricas, motivações e aplicações futuras
            que não ensinam uma habilidade concreta nesta aula.

            Teste de validação (aplique mentalmente a cada item antes de incluir):
            "Consigo criar uma pergunta aberta que avalie se o aluno atingiu isso?"
            Se não → reformule ou descarte.

            ## FORMATO DE SAÍDA

            Responda estritamente no formato estruturado solicitado, sem texto adicional,
            comentários ou explicações fora da estrutura de dados.
        """).strip()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Extraia os pré-requisitos e objetivos de aprendizado do seguinte documento de aula:\n\n{text}")
        ])

        self.chain = self.prompt | self.llm

    async def extract(self, text: str, document_id: int) -> dict:
        self.logger.info(f"Extraindo objetivos para o documento {document_id}")

        try:
            result: DocumentObjectives = await self.chain.ainvoke({"text": text})

            return {
                "prerequisites": result.prerequisites,
                "learning_objectives": result.learning_objectives
            }
        except Exception as e:
            self.logger.exception(f"Falha ao extrair objetivos do documento {document_id}: {e}")
            raise RuntimeError(f"Falha ao extrair objetivos: {e}") from e
