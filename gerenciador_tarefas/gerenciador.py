from enum import Enum
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, constr

from operator import itemgetter


class EstadosPossiveis(str, Enum):
    finalizado = "finalizado"
    nao_finalizado = "não finalizado"

class TarefaEntrada(BaseModel):
    titulo: constr(min_length=3, max_length=50)
    descricao: constr(max_length=140)
    estado: EstadosPossiveis = EstadosPossiveis.nao_finalizado

class Tarefa(TarefaEntrada):
    id: UUID

app = FastAPI()

TAREFAS = [
    {
        "id": "1",
        "titulo": "fazer compras",
        "descrição": "comprar leite e ovos",
        "estado": "não finalizado",
    },
    {
        "id": "2",
        "titulo": "levar o cachorro para tosar",
        "descrição": "está muito peludo",
        "estado": "não finalizado",
    },
    {
        "id": "3",
        "titulo": "lavar roupas",
        "descrição": "estão sujas",
        "estado": "não finalizado",
    },
]


@app.post('/tarefas', response_model=Tarefa, status_code=status.HTTP_201_CREATED)

#Põe em ordem e lista as tarefas
@app.get("/tarefas")
def listar():
    return sorted(TAREFAS)

@app.post('/tarefas')
def criar(tarefa: Tarefa):
    pass


@app.post('/tarefas', response_model=Tarefa, status_code=status.HTTP_201_CREATED)
def criar(tarefa: TarefaEntrada):
    nova_tarefa = tarefa.dict()
    nova_tarefa.update({"id": uuid4()})
    TAREFAS.append(nova_tarefa)
    return nova_tarefa

#deleta tarefa
@app.delete('/tarefas/86d92774-281c-4e5a-87f2-69029177bfd2', status_code=status.HTTP_204_NO_CONTENT)
def deletar(tarefa: TarefaEntrada):
    tarefa_removida = tarefa.dict()
    tarefa_removida.update({"id": '86d92774-281c-4e5a-87f2-69029177bfd2'})
    TAREFAS.remove(tarefa_removida)
    return TAREFAS

#finaliza tarefa
@app.put('/tarefas/86d92774-281c-4e5a-87f2-69029177bfd2', status_code=status.HTTP_200_OK)
def completar(tarefa: TarefaEntrada):
    tarefa_completa = tarefa.dict()
    tarefa_completa.update({"estado": 'finalizado'})
    return TAREFAS

