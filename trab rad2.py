
#IMPORTANDO AS BIBLIOTECAS NECESSARIAS
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

#CRIANDO E FORMATANDO A JANELA
janela = tk.Tk()
janela.geometry("800x600")#TAMANHO DA JANELA
janela.title("Área do Recrutador")#TITULO DA JANELA
janela.configure(bg='light blue')  # COR DA JANELA

#CRIANDO O TITULO DENTRO DA JANELA
titulo_label = tk.Label(janela, text="AREA DO RECRUTADOR", font=("Helvetica", 16, "bold"), bg='light blue')
titulo_label.pack(side="top", fill="x")

#FUNÇÃO CRIADA PARA DAR REAÇÃO DO SISTEMA AO CLICAR EM SALVAR DECISAO
def salvar_decisao():
    decisao = decisao_var.get()
    selected_candidate = tree.item(tree.selection())

    if decisao == "":#SE A DECISAO ESTIVER VAZIA ABRE UM AVISO DE ERRO
        messagebox.showerror("Erro", "Defina uma decisão")
        return

    if selected_candidate:
        candidate_id = selected_candidate['values'][0]
        conn = sqlite3.connect('candidatos.db')
        cursor = conn.cursor()

        #COMANDO PARA REALIZAR A ALTRAÇÃO NO BANCO DE DADOS QUANDO A DECISÃO FOR ESCOLHIDA
        cursor.execute('''
            UPDATE candidatos
            SET decisao = ?
            WHERE id = ?
        ''', (decisao, candidate_id))
        #CONFIRMANDO AS ALTERAÇÕES DENTRO DO BANCO E FECHANDO A CONEXAO
        conn.commit()
        conn.close()

        #ESSA MENSAGEM SERÁ EXIBIDA QUANDO FOR TOMADA A DECISAO
        messagebox.showinfo("Sucesso", "Decisão registrada com sucesso!")
        carregar_candidatos()

#FUNCAO COM O LOOP UTILIZANDO MODULOS DO TKINTER, PARA FILTRAR OS DADOS ATRAVES DO QUE FOR INSERIDO NOS CAMPOS DO FILTRO
def carregar_candidatos():
    for i in tree.get_children():
        tree.delete(i)
    #VARIAVEIS DOS CAMPOS DO FILTRO E O MODULO DO TKINTER QUE LIGA O QUE FOI DIGITADO NOS CAMPOS A VARIAVEL
    filtro_cidade = filtro_cidade_var.get()
    filtro_estado = filtro_estado_var.get()
    filtro_salarial = filtro_salarial_var.get()
    filtro_status = filtro_status_var.get()
    
    #CONEXAO COM O BANCO
    conn = sqlite3.connect('candidatos.db')
    cursor = conn.cursor()

    #QUANDO CLICAR EM FILTRAR ELE VAI BUSCAR EM CADA CAMPO O QUE FOI INSERIDO PELO USUSARIO E BUSCAR NO BANCO DE DADOS DE ACORDO COM O QUE FOI INSERIDO NAS VARIÁVEIS CORRESPONDENTES
    if filtro_cidade:
        cursor.execute('SELECT * FROM candidatos WHERE cidade = ?', (filtro_cidade,))
    elif filtro_estado:
        cursor.execute('SELECT * FROM candidatos WHERE estado = ?', (filtro_estado,))
    elif filtro_salarial:
        cursor.execute('SELECT * FROM candidatos WHERE salario >= ?', (filtro_salarial,))
    elif filtro_status:
        cursor.execute('SELECT * FROM candidatos WHERE status = ?', (filtro_status,))
    else:
        cursor.execute('SELECT * FROM candidatos')
        
    #CANDITADOS VAI ARMAZENAR LISTA DOS REGISTROS ENCONTRATOS NO FILTRO
    candidatos = cursor.fetchall()
    
    #ESSE LOOP ACRESCENTA UMA NOVA LINHA NA TREEVIEW DA JANELA COM AS INFORMACOES CONTIDAS NA VARIAVEL CANDIDATO
    for candidato in candidatos:
        tree.insert('', 'end', values=candidato)

    #FECHANDO CONEXAO
    conn.close()

# CRIANDO AREA PARA CRIAR OS ROTULOS E BOTOES DOS FILTROS
frame_filtros = tk.Frame(janela)
frame_filtros.pack(pady=10)

#CRIANDO OS CAMPOS E OS NOMES QUE REPRESENTARÃO OS CAMPOS A SEREM FILTRADOS
filtro_cidade_label = tk.Label(frame_filtros, text="FILTRAR POR:        Cidade:")
filtro_cidade_label.grid(row=0, column=0)
filtro_cidade_var = tk.StringVar()
filtro_cidade_entry = tk.Entry(frame_filtros, textvariable=filtro_cidade_var)
filtro_cidade_entry.grid(row=0, column=1)

filtro_estado_label = tk.Label(frame_filtros, text="   Estado:")
filtro_estado_label.grid(row=0, column=2)
filtro_estado_var = tk.StringVar()
filtro_estado_entry = tk.Entry(frame_filtros, textvariable=filtro_estado_var)
filtro_estado_entry.grid(row=0, column=3)

filtro_salarial_label = tk.Label(frame_filtros, text="   Salário a partir de:")
filtro_salarial_label.grid(row=0, column=4)
filtro_salarial_var = tk.StringVar()
filtro_salarial_entry = tk.Entry(frame_filtros, textvariable=filtro_salarial_var)
filtro_salarial_entry.grid(row=0, column=5)

filtro_status_label = tk.Label(frame_filtros, text="   Status do Emprego Atual:")
filtro_status_label.grid(row=0, column=6)
filtro_status_var = tk.StringVar()
filtro_status_combobox = ttk.Combobox(frame_filtros, textvariable=filtro_status_var, values=["", "Empregado", "Desempregado", "Informal"])
filtro_status_combobox.grid(row=0, column=7)

#ABAIXO A FUNCAO QUE O BOTÃO APLICAR FILTRO IRÁ RODAR AO SER CLICADO
filtrar_button = tk.Button(frame_filtros, text="Filtrar", command=carregar_candidatos)
filtrar_button.grid(row=0, column=8)

#FORMATAÇÃO A TREEVIEW ONDE SERÃO EXIBIDOS OS RESULTADOS
tree_frame = tk.Frame(janela)
tree_frame.pack(padx=10, pady=10)

#O NOME DE CADA COLUNA PARA EXIBIÇÃO DOS DADOS QUE SERÃO EXIBIDOS NA TREEVIEW
columns = ["ID", "Nome", "Idade", "Cidade", "Estado", "Telefone", "Email", "Experiência", "Expc. Salarial", "Status Atual", "Arquivo", "Decisão"]
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col) #CONFIGURANDO O TEXTO DO CABECALHO DAS COLUAS
    tree.column(col, width=100)#DEFININDO A LARGURA DA COLUNA

tree.pack()

#CRIAÇÃO DO CAMPO DECISAO QUE MOSTRARÁ 3 OPÇÕES
decisao_label = tk.Label(janela, text="Defina a decisão:")
decisao_label.pack()
decisao_var = tk.StringVar()
decisao_combobox = ttk.Combobox(janela, textvariable=decisao_var, values=["", "Aprovado", "Reprovado", "Em análise"])
decisao_combobox.pack()

#DEFININDO O BOTÃOAO DE SALVAR DECISAO E QUAL A FUNÇÃO DENTRO DO CODIGO QUE ELA IRÁ RODAR AO SER CLICADA
salvar_decisao_button = tk.Button(janela, text="Salvar Decisão", command=salvar_decisao)
salvar_decisao_button.pack()



# MANTENDO A JANELA SEMPRE ABERTA
janela.mainloop()
