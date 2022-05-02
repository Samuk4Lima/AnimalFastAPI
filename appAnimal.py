from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4 #gerador de ids hashing automaticos, utilizando a versao 4


app = FastAPI()

class Animal(BaseModel):
    id: Optional[int] #para n dar erro se o usuario nao digitar o id e ser forçado a requisicao no metodo post
    nome: str
    tipo: str
    idade: int
    genero: str
    cor: str


database: List[Animal] = []


@app.get('/animais')
def listaDeAnimais():
    return database

#criando parametro de rota para obter o ID do animal em Questão
@app.get('/animais/{id}')
def obterID(id: str):
    for animal in database:
        if animal.id == id:
            return animal
    return {'error': 'animal não encontrado'}

#criando parametro de rota para deletar por id o animal do database
@app.delete('/animais/{idtoDelete}')
def deleteByID(idtoDelete: str):
    curr = ''
    flag = False
    for subject in database:
        if subject.id == idtoDelete:
            flag = True
            curr = subject.nome
            database.remove(subject)
            break
    if flag:
        return {'msg': f'{curr} foi removido do sistema'}
    else:
        return {'error': 'Componente de ID não encontrado'}



@app.post('/animais')
def cadastrarAnimais(animal: Animal):
    animal.id = str(uuid4())
    database.append(animal)
    return {'msg':f'{animal.nome} foi cadastrado(a) com sucesso'}
