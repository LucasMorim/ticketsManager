import db
import re

def relatorioGeral():

    dados = db.load()
    for data in dados:
        for tipo in dados[data]:
            print("# Data:",data,"\tTipo:",tipo)
            for ticket in dados[data][tipo]:
                print("\tTicket: ", ticket, dados[data][tipo][ticket])

def relatorioGeralPorData(pData):

    dados = db.load()
    if pData in dados.keys():
        for data in dados:
            if pData == data:
                for tipo in dados[data]:
                    print("\n# Data:",data,"\tTipo:",tipo)
                    for ticket in dados[data][tipo]:
                        print("\tTicket: ", ticket, dados[data][tipo][ticket])
    else:
        print("Não tiveram tickets nessa data")
        
def relatorioMediaEsperaPorData(pData):

    sumSegundos = 0
    contador=0
    
    dados = db.load()
    if pData in dados.keys():
        for data in dados:
            if pData == data:
                for tipo in dados[data]:
                    print("Tipo:",tipo)
                    for ticket in dados[data][tipo]:
                        tkt = dados[data][tipo][ticket]
                        if db.BALCAO in tkt:
                            tempEspera = tkt[db.TEMPO_ESPERA]
                            print("\tTicket: ", ticket, tkt[db.TEMPO_ESPERA])
                            numeros = re.findall(r"\d+", tempEspera) 
                            sumSegundos += int(numeros[0]) * 3600
                            sumSegundos += int(numeros[1]) * 60
                            sumSegundos += int(numeros[2])
                            contador+=1
                        
        if contador > 0:
            mediaTempoSec = sumSegundos / contador
            horas = mediaTempoSec//3600
            mediaTempoSec = mediaTempoSec - (horas*3600)
            min = mediaTempoSec // 60
            mediaTempoSec = mediaTempoSec - (min * 60)
            
            print("\n",int(horas), "horas, ", int(min), "minutos e ",int(mediaTempoSec), "segundos de intervalo entre atendimentos")
        else:
            print("Não há dados para calcular a média.")
             
    else:
        print("Não tiveram tickets nessa data")
      
def relatorioAtendBalcoesPorData(pData):
    
    contagemBal = [0, 0, 0, 0]
    
    dados = db.load()
    if pData in dados.keys():
        for data in dados:
            if pData == data:
                for tipo in dados[data]:
                    print("Tipo:",tipo)
                    for ticket in dados[data][tipo]:
                        tkt = dados[data][tipo][ticket]
                        if db.BALCAO in tkt:
                            balc = tkt[db.BALCAO]
                        
                            if balc == "1":
                                contagemBal[0] += 1
                            elif balc == "2":
                                contagemBal[1] += 1
                            elif balc == "3":
                                contagemBal[2] += 1
                            elif balc == "4":
                                contagemBal[3] += 1
                                
            if contagemBal[0] > 0 or contagemBal[1] > 0 or contagemBal[2] > 0 or contagemBal[3] > 0:
                print("\nAtendimentos: ")
                print("Balcão 1: ", contagemBal[0])
                print("Balcão 2: ", contagemBal[1])
                print("Balcão 3: ", contagemBal[2])
                print("Balcão 4: ", contagemBal[3])
    else:
        print("Não tiverem tickets nesse dia!")
                
def relatorioReceitaPorData(pData):
    receita = 0
    
    dados = db.load()
    if pData in dados.keys():
        for data in dados:
            if pData == data:
                for tipo in dados[data]:
                    if tipo == db.ENTREGA:
                        for ticket in dados[data][tipo]:
                            tkt = dados[data][tipo][ticket]
                            if db.VALOR in tkt:
                                receita += tkt[db.VALOR]

                            if receita > 0:
                                print("Receita: ",receita,"€")
                            elif receita == 0:
                                print("Não tiveram atendimento de entregas nesta data")
    else:
        print("Não tiveram tickets nesta data")