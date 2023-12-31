import json
import os
from datetime import datetime

REPARACAO="reparacao"
ENTREGA="entrega"
DATA_FILE="tickets.json"

TIPO_TICKET="tipo"
NUMERO_TICKET="numero_ticket"
DATA_CRIACAO="data_criacao"
BALCAO="balcao"
DATA_ATENDIMENTO="data_atend"
TEMPO_ESPERA="tempo_espera"
EQUIPAMENTO="equipamento"
OBSERVACAO="observacao"
AVARIA="avaria"
CONDICAO="condicao"
VALOR="valor"

global dados

def ler_dados(tipo):
    global dados
    dados = load()
    return dados[tipo]

def load():
    try:
        with open(DATA_FILE, "r") as f:
            dados=json.loads(f.read())
        return dados
    except IOError:
        with open(DATA_FILE, "w") as f:
            dados={REPARACAO: {}, ENTREGA: {}}
            f.write(json.dumps(dados))
        return load()

def gravar(contador, tipo, ticket):
    dados = load()
    dados[tipo][contador] = ticket
    with open(DATA_FILE, "w") as f:
       f.write(json.dumps(dados))

def ultimoTicket(tipo):
    try:
        dados=load()
        lista=dados[tipo]
        return len(lista.keys())
    except:
        return 0

def dataFormatada():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
