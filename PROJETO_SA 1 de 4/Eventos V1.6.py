import FreeSimpleGUI as sg 
import datetime 
import json 
import os
from Cadastro_auto import eventos_auto, locais_auto, datas_auto

#===================#
#-----VARIÁVEIS-----#
#===================#

ARQUIVO_JSON = "eventos.json"
eventos_lista = []             
eventos_quant = [0]*12        
meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
excluidos_quant = [0]*12 
data = None

#=================#
#-----FUNÇÕES-----#
#=================#

def Carregar_JSON(): #Carrega o arquivo eventos.json, caso não tenha ele cria um
    global eventos_lista, eventos_quant, excluidos_quant  

    if not os.path.exists(ARQUIVO_JSON):
        dados_iniciais = {
            "eventos_lista": [],
            "eventos_quant": [0]*12,
            "excluidos_quant": [0]*12
        }
        
        with open(ARQUIVO_JSON, "w", encoding = "utf-8") as f:
            json.dump(dados_iniciais, f, ensure_ascii=False, indent=4)

    with open(ARQUIVO_JSON, "r", encoding = "utf-8") as f:
            dados = json.load(f)                  
            eventos_lista = dados.get("eventos_lista", [])
            eventos_quant = dados.get("eventos_quant", [0]*12)
            excluidos_quant = dados.get("excluidos_quant", [0]*12)

def Salvar_JSON():   
    dados = {
        "eventos_lista": eventos_lista,
        "eventos_quant": eventos_quant,
        "excluidos_quant": excluidos_quant
    }
    with open("eventos.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def Atualizar_Cadastro():
    global tabela
    tabela = [[j[0], j[1], j[2]] for i, j in enumerate(eventos_lista)] # Cria uma lista de listas, onde o i (0, 1, 2...) é o indice, e o j são os valores (evento, local e data) 
    janela['-QUADRO-'].update(values=tabela) # Atualizar o Cadastro. 
    
def Atualizar_Relatorio():
    tabela = []   
    
    for c in range(12):
        tabela.append([meses[c], eventos_quant[c], excluidos_quant [c]]) 
        
    Montar_sub_Relatorio() 
    
    janela["-RELATORIO-"].update(tabela, visible = True)
    janela['-MSG-'].update (visible = False)
    janela['-SUB_RELATORIO-'].update(sub_tabela, visible = True)
    
def Montar_sub_Relatorio(): # Monta a sub-tabela de forma "manual"
    global sub_tabela
    sub_tabela = []
    sub_tabela.append(['Total Marcados', sum(eventos_quant)])
    sub_tabela.append(['Eventos Desmarcados', sum(excluidos_quant)])
    sub_tabela.append (['Total de eventos Cadastrados', sum(eventos_quant) + sum(excluidos_quant)]) 

def Excluir_Cadastro():
    global removed

    item = selecionado[0] 
    removed = eventos_lista.pop(item) 
    Atualizar_Cadastro()

    data = removed[2]               # Pega a data do que foi excluido
    dia, mes, ano = data.split('/') # Cria uma lista separando pelo '/', e distribui o valor na variáveis
    mes = int(mes)                  
    eventos_quant[mes - 1] -= 1 
    excluidos_quant[mes - 1] += 1 
    Atualizar_Relatorio()

    if evento == 'Excluir': 
        sg.popup('Evento deletado!', image='gato_joinha.png')  

def Cadastro_automatico(): 
    global tabela, eventos_quant, eventos_lista
    tabela = []

    for c in range(200):
        evento_atual = eventos_auto[c]
        local = locais_auto[c]
        data = datas_auto[c]
        tabela.append([evento_atual, local, data])
        eventos_lista.append([evento_atual, local, data])

        dia, mes, ano = map(int, data.split('/'))
        eventos_quant[mes - 1] +=1

sg.theme('DarkGreen4')

#================#
#-----LAYOUT-----# 
#================#


layout = [ 
    [sg.Button('.', image_filename='gato_joinha.png'), sg.Text("Bem-vindo ao Cadastro de eventos!", font=('Arial', 18, "bold"), justification='center', expand_x=True), sg.Button('', image_filename='gato_joinha.png')],
    [sg.HorizontalSeparator(pad=(0,10))], 
    [
        sg.TabGroup(
            [[
                sg.Tab('Cadastro', [
                    [sg.Text('Evento:', font=('bold')), sg.Input(key='-EVENTO-', size=(59,1))], 
                    [sg.Text('Local:  ', font=('bold')), sg.Input(key='-LOCAL-', size=(59,1))],
                    [sg.Button('Calendario', button_color='DarkBlue', pad=(10,0), font=('Arial')), sg.Text('Selecione uma data...', font=('bold'), key='-DATA-')],
                    [sg.Button('Cadastrar', font=('Arial'), pad=(10,10)), sg.Button('Excluir', font=('Arial'), pad=(10,10)), sg.Button('Editar',font=('Arial'), pad=(10,10)), sg.Button('Limpar', font=('Arial'), pad=(10,10)), sg.Button('Deletar Tudo', font=('Arial'), pad=(10,10), button_color='red')],
                    [sg.HorizontalSeparator(pad=(0,10))],
                    [sg.Text('Filtro:', font=('bold'), pad=(10,10)), sg.Input(key='-PESQUISA-', enable_events=True)],
                    [sg.Table(values = [], headings = ['EVENTO', 'LOCAL', 'DATA'],  key='-QUADRO-', enable_events=True, auto_size_columns=True, col_widths= 190, row_height=25, expand_x=True, justification='center')], #lista que mostra os eventos cadastrados
                ]),

                sg.Tab('Relatório', [
                    [sg.Text('Adicione pelo menos um evento, para gerar o relatório...', visible = True, key= '-MSG-',font=('Arial', 18,'bold'),justification='center', expand_x=True)],
                    [sg.Table(values=[], headings = ['MESES', 'EVENTOS POR MÊS', 'EVENTOS DESMARCADOS', ],visible = False, key='-RELATORIO-', auto_size_columns=True, col_widths= 190, row_height=25, expand_x=True, justification='center')],
                    [sg.Table(values=[], key= '-SUB_RELATORIO-', visible=False, headings = ['INFORMAÇÕES', 'QUANTIDADE'],auto_size_columns=True, col_widths= 190, row_height = 20,size = (190, 3), expand_x=True, justification='center', pad=(0,30))]
                ]),
    
                sg.Tab('Creditos', [
                    [sg.Text('Participartes do trabalho: \n'
                             '\n'
                             '\n'
                             'Igor Flores\n'
                             '\n'
                             'Lucas da Silva Batista\n' 
                             '\n'
                             'Ulf Gunnar Silva Pettersson\n'
                             '\n'
                             'Pedro Lucas Rodrigues\n'
                             '\n'
                             '\n'
                             '© Grupo do Igor parte II', font=('Arial', 22,'bold'),justification='center', expand_x=True)]
                ]),
            ]], 
        )
    ]
]

janela = sg.Window('Eventos/Compromissos',layout, element_justification='center', icon='calendar.ico', grab_anywhere=True, finalize=True, resizable=True)
Carregar_JSON()
Atualizar_Cadastro()
Atualizar_Relatorio()

#==================#
#-----PROGRAMA-----#
#==================#

while True:
    evento, valores = janela.read()

    if evento == sg.WINDOW_CLOSED:
        break
    
    #============================#
    #-----BOTÃO DE CADASTRAR-----#
    #============================#

    if evento == 'Calendario':
        data = sg.popup_get_date()

        if data:
            mes, dia, ano = map(int, data)
            janela['-DATA-'].update(f'{dia:02d}/{mes:02d}/{ano}') # :02d diz que deve ter no minimo 2 números na variável, caso não tenha ele adiciona um 0 na frente

    #============================#
    #-----BOTÃO DE CADASTRAR-----#
    #============================#

    if evento == 'Cadastrar':
        evento_atual = valores['-EVENTO-']
        local = valores['-LOCAL-']

        if not evento_atual or not local or not data: # Caso esteja faltando alguma informação
            sg.popup('Preencha Todos os Campos!', image='gato_desjoinha.png', text_color='red')
            continue

        if evento_atual and local and dia and mes and ano: # Verifica se os valores foram colocados
            evento_atual = str(evento_atual)
            local = str(local)
            data_atual = str(datetime.date.today())
            ano_atual, mes_atual, dia_atual = data_atual.split('-')

            dia, mes, ano, dia_atual, mes_atual, ano_atual = map(int, (dia, mes, ano, dia_atual, mes_atual, ano_atual))
        
            # Condicionais para verificar se datas são do passado 
            if ano < ano_atual:
                sg.popup('Data invalida', image='gato_desjoinha.png', text_color='red' )
                continue
            if mes < mes_atual and ano <= ano_atual:
                sg.popup('Data invalida', image='gato_desjoinha.png', text_color='red' )
                continue
            if dia < dia_atual and mes <= mes_atual and ano <= ano_atual:
                sg.popup('Data invalida', image='gato_desjoinha.png', text_color='red' )
                continue

            eventos_lista.append([evento_atual, local, f'{dia:02d}/{mes:02d}/{ano}'])

            Atualizar_Cadastro()

            sg.popup('Cadastro completo!', image='gato_joinha.png')

            eventos_quant[mes - 1] += 1
            Atualizar_Relatorio()
            Salvar_JSON()

        # Renicia os valores, se preparando pro próximo cadastro
        janela['-EVENTO-'].update('')
        janela['-LOCAL-'].update('')
        data = None
        dia = 0
        mes = 0
        ano = 0
        janela['-DATA-'].update('Selecione uma data...')
            
    #==========================#
    #-----BOTÃO DE EXCLUIR-----#
    #==========================#

    if evento == 'Excluir':
        selecionado = valores['-QUADRO-']
        
        if selecionado:
            teste = sg.popup_yes_no('Deseja deletar este evento?') # Pede uma confirmação, onde ''Yes'', no nosso programa serve para dar continuidade a ação

            if teste == 'Yes':

                Excluir_Cadastro()
                Salvar_JSON()

            else:
                continue
        else:
            if len(eventos_lista) == 0:
                sg.popup("Cadastre algum evento", image='gato_desjoinha.png', text_color='red')
                continue
            else:
                sg.popup('Selecione um evento!', image='gato_desjoinha.png', text_color='red')
                continue
 
    #=========================#
    #-----BOTÃO DE LIMPAR-----#
    #=========================#
    
    if evento == 'Limpar':
        janela['-EVENTO-'].update('')
        janela['-LOCAL-'].update('')
        data = 0
        janela['-DATA-'].update('Selecione uma data...')
        
    #=========================#
    #-----BOTÃO DE EDITAR-----#
    #=========================#
    
    if evento == 'Editar':
        selecionado = valores['-QUADRO-']
        if selecionado:
                        
            teste = sg.popup_yes_no('Deseja editar este evento?')
        
            if teste == 'Yes':      
                Excluir_Cadastro()
                evento_atual = removed[0]
                local = removed[1]
                janela['-EVENTO-'].update(evento_atual)
                janela['-LOCAL-'].update(local)
                Salvar_JSON()

            else:
                continue
        else:
            sg.popup('Selecione um evento!', image='gato_desjoinha.png', text_color='red')
            continue
    
    #============================#
    #-----FILTRO DE PESQUISA-----#
    #============================#

    if evento == '-PESQUISA-':
        evento_pesquisa = []
        item = valores['-PESQUISA-'].lower()

        for evento, local, data in eventos_lista: # A cada loop, ele joga todos os valores da lista nas variáveis
            if item in evento.lower() or item in local.lower() or item in data: # E elas são verificadas se são iguais com o que foi digitado pelo usuário
                evento_pesquisa.append([evento, local, data])
       
        janela['-QUADRO-'].update(values=evento_pesquisa)

    #=============================#
    #-----CADASTRO AUTOMÁTICO-----#
    #=============================#

    if evento == '.':
        Cadastro_automatico()
        Atualizar_Cadastro()
        Atualizar_Relatorio()
        Salvar_JSON()

    #===============================#
    #-----BOTÃO DE DELETAR TUDO-----#
    #===============================#

    if evento == 'Deletar Tudo':
        if len(eventos_lista) != 0:
                 
            teste = sg.popup_yes_no("Deseja deletar tudo?")
            
            if teste == 'Yes':
                
                for c in range(len(eventos_lista)):
                    removed = eventos_lista.pop()
                    
                    Atualizar_Cadastro()

                    data = removed[2]               
                    dia, mes, ano = data.split('/') 
                    mes = int(mes)                  
                    eventos_quant[mes - 1] -= 1 
                    excluidos_quant[mes - 1] += 1 

                Atualizar_Relatorio()
                Salvar_JSON()
            else:
                continue
        else:
            sg.popup("Cadastre pelo menos um evento!", text_color='red', image='gato_desjoinha.png')
            continue
            
janela.close()