import os
from datetime import datetime
import numpy as np
import re
import db
import manager

def sistemas():
  
  print("\n----------Sistema de tickets----------\n")
  print("1. Gerar ticket")
  print("2. Atender")
  print("3. Gerenciar tickets")
  print("4. Sair")

  escolha = input("\nO que precisa fazer? ")
  if escolha == "1":
    
    if not verificacaoTempo():
      print("\nO sistema está fechado!")
      print("Volte entre as 8:00 e 23:00")
      sistemas()

    ticket()  

  elif escolha == "2":
    balcao()

  elif escolha == "3":
    gerenciamentos()

  elif escolha == "4":  
    exit()
    
  else:
    print("\nOpção inválida")
    sistemas()

def ticket():

  print("\n1. Reparação")
  print("2. Entrega")
  print("3. Voltar\n")

  escolha = input("Qual o serviço? ")

  if escolha == "1":
    novo_ticket(db.REPARACAO)

  elif escolha == "2":
    novo_ticket(db.ENTREGA)

  elif escolha == "3":
    print("\nSaindo...")
    sistemas()

  else:
    print("\nOpção inválida")
    ticket()

def novo_ticket(tipo):
  
  contador = db.ultimoTicket(tipo) + 1
  print("\nTicket de ", tipo," criado!")
  print("Número do ticket: ", contador)
  dados=db.ler_dados(tipo)
 
  ticket={}
  ticket[db.DATA_CRIACAO] = db.dataHoraFormatada()
  dados[contador] = ticket
  db.gravar(contador,tipo, ticket)
  input("\nPressione Enter para continuar")
  os.system("cls")
  sistemas()

def balcao():

  numeroBalcao = input("\nEm qual balcão está atendendo? ")

  if numeroBalcao != "1" and numeroBalcao != "2" and numeroBalcao != "3" and numeroBalcao != "4": 
    print("Digite um valor válido")
    balcao()

  print("\n1. Reparacao")
  print("2. Entrega")
  tipo = input("\nQual o tipo do ticket? ")
  tipoDb = ""
  if tipo=="1":
    tipoDb=db.REPARACAO
  elif tipo=="2":
    tipoDb=db.ENTREGA

  if (tipoDb == db.REPARACAO and numeroBalcao == "4"):
    print("\nEste balcão não pode atender este tipo de ticket!")
    print("Balcões de 1 a 3")
    balcao()
    
  numero_ticket = input("\nQual o número do ticket? ")
  listaTickets = db.ler_dados(tipoDb)
  ticket=None
  if listaTickets == None or numero_ticket in listaTickets.keys():
    ticket = listaTickets[numero_ticket]
  if ticket == None:
    print("Ticket não encontrado")
    balcao()
  
  
  elif tipoDb == db.REPARACAO:
    balcao_reparacao(ticket)
  elif tipoDb == db.ENTREGA:
    balcao_entrega(ticket)
  else:
    print("Digite um valor válido.")
    balcao()

  ticket[db.BALCAO] = numeroBalcao
  ticket[db.DATA_ATENDIMENTO] = db.dataHoraFormatada()
  ticket[db.TEMPO_ESPERA] = str(tempoDeEspera(ticket))

  db.gravar(numero_ticket, tipoDb, ticket)

  input("\nPressione Enter para continuar")
  os.system("cls")

  sistemas()

def balcao_reparacao(ticket):  
  while True:
    equip = input("\nQual o equipamento reparado? ")
    try:
      equip = int(equip)
      print("Inválido! Não coloque somente números!")
    except ValueError:
      ticket[db.EQUIPAMENTO] = equip
      break

  while True:
    avaria = input("Descreva a avaria: ")
    try:
      avaria = int(avaria)
      print("Inválido! Não coloque somente números!")
    except ValueError:
      ticket[db.AVARIA] = avaria
      break

  while True:
    obs = input("Alguma observação adicional? ")
    try:
      obs = int(obs)
      print("Inválido! Não coloque somente números!")
    except ValueError:
      ticket[db.OBSERVACAO] = obs
      break
    
def balcao_entrega(ticket):
  while True:
    condicao = input("\nQual a condição do equipamento? ")
    try:
      int(condicao)
      print("Inválido! Não coloque somente números!")
    except ValueError:
      ticket[db.CONDICAO] = condicao
      break

  while True:
    obs = input("Alguma observação adicional? ")
    try:
      int(obs)
      print("Inválido! Não coloque somente números!")
    except ValueError:
      ticket[db.OBSERVACAO] = obs
      break

  while True:
    try:
      valor = float(input("Qual o valor a ser pago: "))
      ticket[db.VALOR] = valor
      break
    except ValueError:
      print("\nDigite um valor válido!")
  
def tempoDeEspera(ticket):
  dataIni = datetime.strptime(ticket[db.DATA_CRIACAO], "%d/%m/%Y %H:%M:%S")
  dataFim = datetime.strptime(ticket[db.DATA_ATENDIMENTO], "%d/%m/%Y %H:%M:%S")
  tempo_espera = dataFim - dataIni
  return tempo_espera

def verificacaoTempo():
  agora = datetime.now()
  return agora.hour >= 8 and agora.hour < 23

def gerenciamentos():
  
    while True:
        try:
            print("\nGerenciamentos: ")
            print("1. Relatório geral de tickets")
            print("2. Relatório geral de tickets por data")
            print("3. Relatório de média de espera por data")
            print("4. Relatório de atendimento de balcões por data")   
            print("5. Relatório de receita por data")
            print("6. Voltar")
            geren = int(input("\nEscolha o gerenciamento: "))
            if geren == 1:
                manager.relatorioGeral()
            elif geren == 2:
                data = input("Digite a data no formato AAAA-MM-DD:")
                manager.relatorioGeralPorData(data)
            elif geren == 3:
                data = input("Digite a data no formato AAAA-MM-DD:")
                manager.relatorioMediaEsperaPorData(data)
            elif geren == 4:
                data = input("Digite a data no formato AAAA-MM-DD:")
                manager.relatorioAtendBalcoesPorData(data)
            elif geren == 5:
                data = input("Digite a data no formato AAAA-MM-DD:")
                manager.relatorioReceitaPorData(data)
            elif geren == 6:
                os.system("cls")
                sistemas()
            else:
                print("Opção inválida")
            input("\nPressione Enter para continuar")
            os.system("cls")
        except ValueError:
            print("\nValor inválido")
            gerenciamentos()


sistemas()
