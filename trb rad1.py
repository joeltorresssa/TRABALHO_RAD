#IMPORTANDO BIBLIOTECAS NECESSARIAS
import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3


#CRIANDO A VARIAVEL DA JANELA NO METODO TK
#CRIANDO NOME DA JANELA, TAMANHO E COR
janela = tk.Tk()
janela.title("Área do Candidato")
janela.geometry("900x900")
janela.configure(bg="light blue")

#ADICIONANDO O TITULO NA PRIMEIRA LINHA DA JANELA E FORMATANDO O TEXTO
titulo_label = tk.Label(janela, text="Área do Candidato", font=("Arial", 17, "bold"))
titulo_label.pack()


def salvar_dados():# NOME DA FUNÇÃO QUE VAI SALVAR NAS VARIAVEIS OD DADOS INSERIDOS NOS CAMPOS

#CRIANDO AS VARIAVEIS E OS METODOS UTILIZADO PARA FAZER A LIGAÇÃO DE CADA CAMPO A SUA RESPECTIVA VARIAVEL
    nome = nome_digitado.get()
    idade = idade_digitada.get()
    cidade = cidade_digitada.get()
    estado = estado_digitado.get()
    telefone = telefone_digitado.get()
    email = email_digitado.get()
    experiencia = experiencia_digitada.get("1.0", tk.END).strip()
    salario = salario_digitado.get()
    arquivo_dados = entrada_arquivo_dados.get()  #VARIAVEL QUE VAI OBTER O ARQUIVO
    status = status_inserido.get()
    decisao = ""  # INICIA VAZIO




# SE TODOS OS CAMPOS NÃO FOREM PREENCHIDOS DEVE APARECER UMA MSG DE ERRO ("Todos os campos devem ser preenchidos")
    if not all((nome, idade, cidade, estado, telefone, email, experiencia, salario, arquivo_dados, status)):
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return

# FAZENDO CONEXAO COM O BANCO DE DADOS
    conexao = sqlite3.connect('candidatos.db')
    cursor = conexao.cursor() #CRIANDO O CURSOR PARA REALIZAR OS COMANDO DENTRO DO BANCO DE DADOS

#COMANDO QUE CRIA A TABELA DENTRO DO DO BANCO DE DADOS CASO ELA NÃO EXISTA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            cidade TEXT,
            estado TEXT,
            telefone TEXT,
            email TEXT,
            experiencia TEXT,
            salario TEXT,
            arquivo BLOB,
            status TEXT,
            decisao TEXT
        )
    ''')

#ESTE É O COMANDO QUE IRÁ INSERIR NO BANCO DE DADOS OS DADOS QUE FORAM INSERIDOS NOS CAMPOS.
#CADA DADO DAS VARIÁVEIS IRÁ SUBSTITUIR OS VALORES
    cursor.execute('''
        INSERT INTO candidatos (nome, idade, cidade, estado, telefone, email, experiencia, salario, arquivo, status, decisao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, idade, cidade, estado, telefone, email, experiencia, float(salario), arquivo_dados, status, decisao))

#ABAIXO ESTAMOS CONFIRMANDO AS ALTERAÇÕES FEITAS NO BANCO DE DADOS E FECHANDO A CONEXÃO
    conexao.commit()
    conexao.close()

#APOS SAVAR OS DADOS INSERIDOS, PEÇO PARA ZERAR OS CAMPOS DEIXANDO TODOS EM BRANCO
    nome_digitado.delete(0, tk.END)
    idade_digitada.delete(0, tk.END)
    cidade_digitada.delete(0, tk.END)
    estado_digitado.delete(0, tk.END)
    telefone_digitado.delete(0, tk.END)
    email_digitado.delete(0, tk.END)
    experiencia_digitada.delete("1.0", tk.END)
    salario_digitado.delete(0, tk.END)
    arquivo_label.config(text="Nenhum arquivo selecionado")
    status_inserido.set("Empregado")
    entrada_arquivo_dados.set(b"")

    messagebox.showinfo("Sucesso", "Dados do candidato foram salvos com sucesso!")#MSG QUE APARACE AO CLICAR EM SALVAR

#NOME DA FUNÇÃO QUE SERA USADA PARA SAVAR O ARQUIVO NO BANCO E DEFINE O TIPO DO ARQUIVO QUE PODE SER ANEXADO AO BANCO
def selecionar_arquivo():
    arquivo_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
    with open(arquivo_path, 'rb') as file:
        arquivo_dados = file.read()
        entrada_arquivo_dados.set(arquivo_dados)
    arquivo_label.config(text=arquivo_path)

#CRIANDO O NOME DOS CAMPOS, CADA DADO INSERIDO NOS CAMPOS SERÃO ARMAZENADO NAS SUAS RESPECTIVAS VARIAVEIS
#NOME
nome_label = tk.Label(janela, text="Nome:")
nome_label.pack()
nome_digitado = tk.Entry(janela)
nome_digitado.pack()
#IDADE
idade_label = tk.Label(janela, text="Idade:")
idade_label.pack()
idade_digitada = tk.Entry(janela)
idade_digitada.pack()
#CIDADE
cidade_label = tk.Label(janela, text="Cidade:")
cidade_label.pack()
cidade_digitada = tk.Entry(janela)
cidade_digitada.pack()
#ESTADO
estado_label = tk.Label(janela, text="Estado:")
estado_label.pack()
estado_digitado = tk.Entry(janela)
estado_digitado.pack()
#TELEFONE
telefone_label = tk.Label(janela, text="Telefone:")
telefone_label.pack()
telefone_digitado = tk.Entry(janela)
telefone_digitado.pack()
#EMAIL
email_label = tk.Label(janela, text="Email:")
email_label.pack()
email_digitado = tk.Entry(janela)
email_digitado.pack()
#EXPERIENCIA
experiencia_label = tk.Label(janela, text="Experiência Profissional:")
experiencia_label.pack()
experiencia_digitada = tk.Text(janela, height=5, width=40)
experiencia_digitada.pack()
#STATUS DO EMPREGO ATUAL
status_label = tk.Label(janela, text="Status de Emprego Atual:")
status_label.pack()
status_inserido = tk.StringVar(value="Empregado")
status_empregado = tk.Radiobutton(janela, text="Empregado", variable=status_inserido, value="Empregado")
status_desempregado = tk.Radiobutton(janela, text="Desempregado", variable=status_inserido, value="Desempregado")
status_informal = tk.Radiobutton(janela, text="Informal", variable=status_inserido, value="Informal")
status_empregado.pack()
status_desempregado.pack()
status_informal.pack()
#EXPECTATIVA SALARIAL
salario_label = tk.Label(janela, text="Expectativa Salarial:")
salario_label.pack()
salario_digitado = tk.Entry(janela)
salario_digitado.pack()

arquivo_label = tk.Label(janela, text="Nenhum arquivo selecionado")#INICIA O ROTULO COM O NOME ESPECIFICADOS
arquivo_label.pack()#CRIANDO O ROTULO DENTRO DA JANELA
entrada_arquivo_dados = tk.StringVar(value=b"")  #O NOME DO ARQUIVO INICIA VAZIO
selecionar_arquivo_button = tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo)
selecionar_arquivo_button.pack()

#CRIANDO O BOTÃO SALVAR E QUAL A FUNÇÃO QUE ELA IRÁ RODAR AO SER CLICADA
salvar_button = tk.Button(janela, text="Salvar", command=salvar_dados)
salvar_button.pack()

# MANTENDO A JANELE SEMPRE ATIVA
janela.mainloop()
