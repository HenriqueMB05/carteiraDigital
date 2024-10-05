import json
import os

carteira ={}
opc = ['Criar usuário','Operações entre contas', 'Sair']
operacoes = ['transferir', 'receber','ver saldo','excluir usuario','sair']

# limpar o terminal
def limpar():
    return os.system('cls')

# Criação de usuário, para conseguir realizar as operações entre si
def criaruser():
    while True:
        nome = str(input("Digite o nome da carteira: ")).strip().capitalize()
        if nome in carteira:
            print('Não foi possivel criar um usuário.\ntente novamente!')
        elif nome not in carteira:
            print(f"Usuário {nome} criado com sucesso")
            carteira.update({nome:{"saldo":5000,"historico":{"transferido":[],"recebido":[]}}})
            break
        elif not nome:
            print("Você não informou nenhum nome de usuário")
            break


def mostraruser():
    print("Usuários")
    for i in carteira.keys():
        print(i, end='-')
        print(f'R${carteira[i]["saldo"]:,.2f}')
    print('-'*25)


def transf(nome1, nome2):
    if nome2 in carteira and nome1 in carteira:
        print(f'O seu saldo disponivel: R${carteira[nome1]['saldo']:.2f}')
        transferir = float(input("O quanto você quer transferir\n>>> ")) 
        if carteira[nome1]['saldo']>=transferir:
            carteira[nome1]['saldo'] -= transferir
            carteira[nome2]['saldo'] += transferir
            carteira[nome1]['historico']['transferido'].append(transferir)
            carteira[nome2]['historico']['recebido'].append(transferir)
            print(f"saldo atual de {nome1}: R${carteira[nome1]['saldo']:,.2f} ")
            print(f"saldo atual de {nome2}: R${carteira[nome2]['saldo']:,.2f} ")
            input()
        else:
            print(f"{nome} não tem saldo suficiente para realizar essa transferencia!")
            input()                            
    elif nome2 not in carteira or nome1 not in carteira:
        print(f"Usuário {nome1}/{nome2} inexistente!")
        input()
    elif not nome2 and not nome1:
        print("Rapaz")
        input()
        return
    

try:
    with open('./carteira.json', 'r') as file:
        files = file.read()
        carteira = json.loads(files)

except:
    limpar()
    if len(carteira)==0:
        criaruser()    
while True:
    limpar()
    # mostra o primeiro menu de opções
    for i, k in enumerate(opc):
            print(f"{i+1} - {k}")
    try:
        esc= int(input(">>> "))
        limpar()
        match esc:
            #Criar um novo usuário
            case 1:
                mostraruser()
                criaruser()

            # Mostra o menu com as operações
            case 2:
                for i, k in enumerate(operacoes):
                    print(f"{i+1} - {k.capitalize()}")
                chc = int(input(">>> "))
                limpar()
                match chc:
                    #Transferir para outro usuário, mostra os usuários disponivel na tela, e em uma linha pede de quem para quem será transferido o valor caso tenha o saldo disponivel será realizada a transferencia se não voltará para a tela inicial
                    case 1:
                        while True:
                            mostraruser()
                            print("Quem vai traferir para quem:")
                            print("Deixe a caixa em branco para sair da operação: ")
                            try:
                                nome1, nome2 = input(">>> ").split(' ')
                            except ValueError as err:
                                print(err)
                                break
                            transf(nome1, nome2)
                            break
                    # Um usuário irá receber o valor de outro usuário, pedindo o nome de quem vai receber de quem irá tirar o valor do primeiro e inserir na conta do segundo
                    case 2:
                        mostraruser()
                        print("Quem vai receber de quem: ")
                        print("Deixe a caixa em branco para sair da operação: ")
                        try:
                            nome1, nome2 = input(">>> ").split(' ')
                        except ValueError as err:
                            print(err)
                            break   
                        transf(nome2, nome1)
                        break
                    case 3:
                        mostraruser()
                        print('De quem você deseja ver o saldo: ')
                        print("Deixe a caixa em branco para sair da operação")
                        nome = str(input(">>> "))
                        if nome in carteira:
                            print(f"|{nome:^20}|")
                            print(f"Saldo: R${carteira[nome]['saldo']:,.2f}")
                            input()
                        elif nome not in carteira:
                            print(f"Usuário {nome} inexistente")
                            input()
                        elif not nome:
                            break
                    case 4:
                        mostraruser()
                        print("Qual usuário você deseja excuir:")
                        print("Deixe a caixa em branco para sair da operação")
                        nome = str(input(">>> ")) 
                        if nome in carteira:
                            print("Digite confirmar para realizar essa ação:")
                            conf = str(input(">>> ")).strip().lower()
                            if conf in 'confirmar':
                                del(carteira[nome])
                                print(f"Usuário {nome} foi excluido com sucesso")
                                input()
                            elif conf not in 'confirmar' or not conf:
                                print(f'Usuário: {nome} não foi excluido')
                                input()
                                break
                    case 5: 
                        break
            case 3:
                break
    except ValueError:
        print('valor inválido')
        input()
try:
    # escreve em um arquivo json para quando o programa for aberto novamente os dados estejam lá
    with open('Carteira.json', 'w') as file:
        file.write(json.dumps(carteira))
except IndexError:
    print('finalizando programa')