import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

class Application():

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        self.root = Tk()
        self.my_tree = ttk.Treeview(self.root)
        self.tela()
        self.quadros()
        self.botoes()
        self.label_entry()
        self.conexao()
        self.root.mainloop()


    def conexao(self):
        self.conexao = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.conexao
       


    def tela(self):
        self.root.geometry("720x640")
        self.root.title("Gerenciador de Restaurante")
        self.root.configure(background='#005089')
        self.root.resizable(False, False)
        self.root.wm_maxsize(1188,792)
        self.root.wm_minsize(640,480)

    def quadros(self):
        self.quadro_1 = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_1.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.4)

        self.quadro_2 = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_2.place(relx=0.03, rely=0.48, relwidth=0.94, relheight=0.49)

    def botoes(self):
        self.bt_limpar = Button(self.quadro_1, text='Limpar', width=7)
        self.bt_limpar.grid(row=3,column=3, columnspan=1,padx=10,pady=5)
        
        self.bt_selecionar = Button(self.quadro_1, text='Selecionar', width=7)
        self.bt_selecionar.grid(row=4,column=3,columnspan=1,padx=10,pady=5)
        
        self.bt_buscar = Button(self.quadro_1, text='Buscar', width=7)
        self.bt_buscar.grid(row=5,column=3,columnspan=1,padx=10,pady=5)

        self.bt_adicionar = Button(self.quadro_1, background="#32CD32", text='Adicionar', width=7)
        self.bt_adicionar.grid(row=3,column=4,columnspan=1,padx=10,pady=5)
 
        self.bt_editar = Button(self.quadro_1, background="#FFA500", text='Editar', width=7)
        self.bt_editar.grid(row=4,column=4,columnspan=1,padx=10,pady=5)

        self.bt_deletar = Button(self.quadro_1, background="#FF0000", text='Deletar', width=7)
        self.bt_deletar.grid(row=5,column=4,columnspan=1,padx=10,pady=5)

    def label_entry(self):
        #           lABEL DO CADASTRO DE FUNCIONÁRIOS
        self.funcionarioIdLabel = Label(self.quadro_1,text="ID Funcionário",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.funcionarioIdLabel.grid(row=3,column=0,columnspan=1,padx=0,pady=5)

        self.funcionarioNomeLabel = Label(self.quadro_1,text="Nome",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.funcionarioNomeLabel.grid(row=4,column=0,columnspan=1,padx=0,pady=5)

        self.cargo_funcLabel = Label(self.quadro_1,text="Cargo",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.cargo_funcLabel.grid(row=5,column=0,columnspan=1,padx=0,pady=5)

        self.salariofuncLabel = Label(self.quadro_1,text="Salário",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.salariofuncLabel.grid(row=6,column=0,columnspan=1,padx=0,pady=5)
        
        
        #           ENTRY DOS FUNCIONÁRIOS
        self.funcionarioIdEntry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.funcionarioIdEntry.grid(row=3,column=1,columnspan=1,padx=0,pady=5)

        self.funcionarioNomeEntry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.funcionarioNomeEntry.grid(row=4,column=1,columnspan=1,padx=0,pady=5)

        self.cargo_funEntry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.cargo_funEntry.grid(row=5,column=1,columnspan=1,padx=0,pady=5)

        self.salario_funcEntry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.salario_funcEntry.grid(row=6,column=1,columnspan=1,padx=0,pady=5)
