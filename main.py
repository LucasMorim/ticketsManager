import os
from datetime import datetime
import numpy as np
from numpy.core.fromnumeric import var
import re
import json

info = []
contBal = [0,0,0,0]
contadorReparacao = 0
contadorEntrega = 0


def sistemas():
  
  print("\nSistemas: ")
  print("1. Ticket")
  print("2. Gerenciamentos")
  print("3. Sair")

  escolha = input("Escolha o sistema: ")
  if escolha == "1":
    
    if not verificateTempo():
      print("\nO sistema está fechado!")
      print("Volte entre as 8:00 e 23:00")
      sistemas()

    ticket()  

  elif escolha == "2":
    gerenciamentos()

  elif escolha == "3":  
    exit()
  else:
    print("\nOpção inválida")
    sistemas()

def ticket():

  print("\nServiços: ")
  print("1. Reparação")
  print("2. Entrega")
  print("3. Voltar\n")

  escolha = input("Digite o serviço: ")

  if escolha == "1":
    atendTicket("Reparacao", reparacao())

  elif escolha == "2":
    atendTicket("Entrega", entrega())

  elif escolha == "3":
    print("\nSaindo...")
    sistemas()

  else:
    print("\nOpção inválida")
    ticket()

def reparacao():
  
  global contadorReparacao

  dados = {}

  contadorReparacao += 1
  print("\nTicket de reparação criado!")
  print("Número do ticket: ", contadorReparacao)
  dados["Tipo"] = "Reparacao"
  dados["Numero Ticket"] = contadorReparacao
  dataIni = datetime.now()
  dataIni = dataIni.strftime("%d/%m/%Y %H:%M:%S")
  dados["Data Criacao"] = dataIni

  return dados

def entrega():

  global contadorEntrega

  dados = {}

  contadorEntrega += 1
  print("\nTicket de entrega criado!")
  print("Número do ticket: ", contadorEntrega)
  dados["Tipo"] = "Entrega"
  dados["Numero Ticket"] = contadorEntrega
  dataIni = datetime.now()
  dataIni = dataIni.strftime("%d/%m/%Y %H:%M:%S")
  dados["Data Criacao"] = dataIni
  
  return dados

def atendTicket(tipo, dados):

  global contBal
  
  balcao = input("\nDigite o balcão: ")

  if balcao != "1" and balcao != "2" and balcao != "3" and balcao != "4": 
    print("Digite um valor valido")
    atendTicket(tipo, dados)

  

  if (tipo == "Reparacao"):
    if (balcao == "4"):
      print("\nEste balcão não pode atender este tipo de ticket!")
      print("Balcões de 1 a 3")
      atendTicket(tipo, dados)


    while True:
      equip = input("\nDigite o equipamento reparado: ")
      try:
        equip = int(equip)
        print("Inválido! Não coloque somente números!")
      except ValueError:
        dados["Equipamento"] = equip
        break

    while True:
      avaria = input("Digite o avaria: ")
      try:
        avaria = int(avaria)
        print("Inválido! Não coloque somente números!")
      except ValueError:
        dados["avaria"] = avaria
        break

    while True:
      obs = input("Digite as observações: ")
      try:
        obs = int(obs)
        print("Inválido! Não coloque somente números!")
      except ValueError:
        dados["Observacao"] = obs
        break
  
  
  else:
    
    while True:
      cond = input("Digite a condição do equipamento: ")
      try:
        cond = int(cond)
        print("Inválido! Não coloque somente números!")
      except ValueError:
        dados["Condicao"] = cond
        break

    while True:
      obs = input("Digite as observações: ")
      try:
        avaria = int(obs)
        print("Inválido! Não coloque somente números!")
      except ValueError:
        dados["Observacao"] = obs
        break

    while True:
      try:
        valor = float(input("Digite o valor a ser pago: "))
        dados["Valor"] = valor
        break
      except ValueError:
        print("\nDigite um valor válido!")

  
  contBal[int(balcao) - 1] += 1

  dataFim = datetime.now()
  dataFim = dataFim.strftime("%d/%m/%Y %H:%M:%S")

  dados["Balcao"] = balcao
  dados["Data Final"] = dataFim
  dados["Tempo de Espera"] = str(tempoDeEspera(dados))

  f = open(f"TICKETS.txt", "a")
  f.write(json.dumps(dados) + "\n")
  f.close()

  os.system("clear")
  organizador(dados)


  sistemas()

def tempoDeEspera(dados):

  dataIni = datetime.strptime(dados["Data Criacao"], "%d/%m/%Y %H:%M:%S")
  dataFim = datetime.strptime(dados["Data Final"], "%d/%m/%Y %H:%M:%S")
  tempo_espera = dataFim - dataIni
  return tempo_espera

def gerenciamentos():

 while True:
    try:
      print("\nGerenciamentos: ")
      print("1. Mapa total de tickets")
      print("2. Mapa de tickets por data")
      print("3. Mapa de média de espera entre atendimento por data")
      print("4. Mapa de atendimento de balcões por data")   
      print("5. Mapa de receitas de produtos entregues por data")
      print("6. Voltar")
      geren = int(input("\nEscolha o gerenciamento: "))
      if geren == 1:
        f = open("TICKETS.txt", "r")
        print(f.read())
        input("Pressione Enter para continuar")
      elif geren == 2:
        procurarMostrar()
      elif geren == 3:
        calcularMediaEspera()
      elif geren == 4:
        contBalcao()
      elif geren == 5:
        calcularReceita()
      elif geren == 6:
        os.system("clear")
        sistemas()
      else:
        print("Opção inválida")
    except ValueError:
      print("\nValor inválido")
      gerenciamentos()

def organizador(obj):
  global info
  info.append(obj)

def procurarMostrar():
    partes = []


    contador = 0
    with open("TICKETS.txt", "r") as f:
        dia1 = input("Digite o dia: ")
        mes1 = input("Digite o mês: ")
        ano1 = input("Digite o ano: ")

        if len(dia1) == 1:
          dia1 = "0"+dia1  
        for x in f:
          partes = json.loads(x)
          numeros = re.findall(r"\d+", partes["Data Criacao"])
          dia2 = numeros[0]
          mes2 = numeros[1]
          ano2 = numeros[2]
          if dia1 == dia2 and mes1 == mes2 and ano1 == ano2:
           print("\n",x)
           contador += 1
    if contador == 0:
      print("\nNão há tickets para essa data!")
    input("Pressione Enter para continuar")

def calcularMediaEspera():
    partes = []
    contador = 0

    sumSegundos = 0

    with open("TICKETS.txt", "r") as f:
        dia1 = input("Digite o dia: ")
        mes1 = input("Digite o mês: ")
        ano1 = input("Digite o ano: ")

        if len(dia1) == 1:
          dia1 = "0"+dia1  
        for x in f:
          partes = json.loads(x)
          numeros = re.findall(r"\d+", partes["Data Criacao"])
          dia2 = numeros[0]
          mes2 = numeros[1]
          ano2 = numeros[2]
          if dia1 == dia2 and mes1 == mes2 and ano1 == ano2:
            partes = x.split(",")
            tempEsp_str = partes[-1]
            numeros = re.findall(r"\d+", tempEsp_str)
            sumSegundos += int(numeros[0]) * 360
            sumSegundos += int(numeros[1]) * 60
            sumSegundos += int(numeros[2])
            contador+=1

    if contador > 0:
        mediaTempoSec = sumSegundos / contador
        min = mediaTempoSec // 60
        seg = mediaTempoSec % 60
        horas = min // 60
        if horas > 1:
            min = min % 60

        print(int(horas), "horas, ", int(min), "minutos e ",int(seg), "segundos de intervalo entre atendimentos")
    else:
        print("Não há dados para calcular a média.")
    input("Pressione Enter para continuar")
 
def contBalcao():
    
    contagemBal = [0, 0, 0, 0]

    with open("TICKETS.txt", "r") as f:
        dia1 = input("Digite o dia: ")
        mes1 = input("Digite o mês: ")
        ano1 = input("Digite o ano: ")

        if len(dia1) == 1:
          dia1 = "0"+dia1  
        for x in f:
          partes = json.loads(x)
          numeros = re.findall(r"\d+", partes["Data Criacao"])
          dia2 = numeros[0]
          mes2 = numeros[1]
          ano2 = numeros[2]
          if dia1 == dia2 and mes1 == mes2 and ano1 == ano2:
                numeros = partes['Balcao']

                for numero in numeros:
                    numero_int = int(numero)

                    if numero_int == 1:
                        contagemBal[0] += 1
                    elif numero_int == 2:
                        contagemBal[1] += 1
                    elif numero_int == 3:
                        contagemBal[2] += 1
                    elif numero_int == 4:
                        contagemBal[3] += 1
    if contagemBal[0] > 0 or contagemBal[1] > 0 or contagemBal[2] > 0 or contagemBal[3] > 0:
      print("\nAtendimentos: ")
      print("Balcão 1: ", contagemBal[0])
      print("Balcão 2: ", contagemBal[1])
      print("Balcão 3: ", contagemBal[2])
      print("Balcão 4: ", contagemBal[3])
    else:
      print("\nNão tiverem tickets nesse dia!")
    input("Pressione Enter para continuar")

def calcularReceita():
    partes = []
    contador = 0

    sumReceita = 0

    with open("TICKETS.txt", "r") as f:
        dia1 = input("Digite o dia: ")
        mes1 = input("Digite o mês: ")
        ano1 = input("Digite o ano: ")

        if len(dia1) == 1:
          dia1 = "0"+dia1  
        for x in f:
          partes = json.loads(x)
          numeros = re.findall(r"\d+", partes["Data Criacao"])
          dia2 = numeros[0]
          mes2 = numeros[1]
          ano2 = numeros[2]

          if dia1 == dia2 and mes1 == mes2 and ano1 == ano2 and partes["Tipo"] == "Entrega":
            valor = partes['Valor']
            sumReceita += valor
            contador+=1

    if contador > 0:
      print("A receita do dia selecionado foi: ",sumReceita,"€")
    else:
      print("Não tiveram tickets nesse dia!")
    input("Pressione Enter para continuar")

def verificateTempo():
  agora = datetime.now()
  return agora.hour >= 8 and agora.hour < 23


sistemas()