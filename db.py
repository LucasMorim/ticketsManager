import json
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

#lê o arquivo e devolve os dados por tipo
def ler_dados(tipo):
    global dados
    dados = load()
    if not dataAtual() in dados.keys():
        dados[dataAtual()] = {tipo: {}}
    if tipo in dados[dataAtual()].keys():
        return dados[dataAtual()][tipo]
    else:
        return None

#lê ou cria o arquivo de dados e passa para o ler_dados
def load():
    try:
        with open(DATA_FILE, "r") as f:
            dados=json.loads(f.read())
        return dados
    except IOError:
        with open(DATA_FILE, "w") as f:
            dados={ dataAtual(): { REPARACAO: {}, ENTREGA: {}}}
            f.write(json.dumps(dados))
        return load()
    
#grava e reescreve o json
def gravar(contador, tipo, ticket):
    dados = load()
    try:
        dados[dataAtual()][tipo][contador] = ticket
    except:
        if not dataAtual() in dados.keys():
            with open(DATA_FILE, "w") as f:
                dados[dataAtual()] = { REPARACAO: {}, ENTREGA: {}}
                f.write(json.dumps(dados))
    with open(DATA_FILE, "w") as f:
        f.write(json.dumps(dados))
    
    


#verifica qual o ultimo ticket criado, para n repetir o cod (apartir do len)
def ultimoTicket(tipo):

    try:
        dados=load()
        if dataAtual() in dados.keys():
            lista=dados[dataAtual()][tipo]
            return len(lista.keys())
        else:
            return 0
    except:
        return 0

#formata a data
def dataHoraFormatada():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def dataAtual():
    return fmtData(datetime.now())

def fmtData(data):
    return data.strftime("%Y-%m-%d")
