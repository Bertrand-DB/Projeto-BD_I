import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

#Nome da tabela e colunas
TABELA = ["Funcionários", "Id_Funcionários", "Nome", "Cargo", "Salário"]

#Dados de conexão
HOST = "localhost"
USER = "root"
PASSWORD = "369MyRoot*"
DATABASE = "Projeto-BD_I"

#constantes de posição dos botões
LARGURA_BT = 0.12
ALTURA_BT = 0.14
ESPACAMENTO_BT = 0.02
X_BOTAO = 1 - LARGURA_BT - ESPACAMENTO_BT

#constantes de posição das labels e entrys
ESPACAMENTO_LB = 0.08
LARGURA_LABEL = 0.18
ALTURA_LABEL = 0.1
X_LABEL = 0.02


class funcoes():
    
    def clear_entry(self):
        self.func_Id_Entry.delete(0,END)
        self.func_Nome_Entry.delete(0,END)
        self.func_Cargo_Entry.delete(0,END)
        self.func_Salario_Entry.delete(0,END)

    def conexao(self):
        self.conn = mysql.connector.connect(
            host = HOST,
            user = USER,
            password= PASSWORD,
            database= DATABASE
        )
        self.cursor= self.conn.cursor()

    def insert_func(self):
        self.func_Id = self.func_Id_Entry.get()
        self.func_Nome = self.func_Nome_Entry.get()
        self.func_Cargo = self.func_Cargo_Entry.get()
        self.func_Salario = self.func_Salario_Entry.get()
        self.conexao()
        self.consulta ="INSERT INTO "+TABELA[0]+" ("+TABELA[1]+","+TABELA[2]+","+TABELA[3]+","+TABELA[4]+")VALUES(%s,%s,%s,%s)"
        self.valores=(self.func_Id,self.func_Nome,self.func_Cargo,self.func_Salario)
        self.cursor.execute(self.consulta,self.valores)
        self.conn.commit()
        self.conn.close()

    def delete_func(self):
        self.func_delete = self.func_Id_Entry.get()
        self.conexao()
        self.consulta = "DELETE FROM "+TABELA[0]+" WHERE "+TABELA[1]+" = %s "
        self.valores = [self.func_delete]
        self.cursor.execute(self.consulta,self.valores)
        self.conn.commit()
        self.conn.close()

class Application(funcoes):

    def __init__(self):
        self.root = tk.Tk()
        self.tela()
        self.quadros()
        self.botoes()
        self.label_entry()
        self.lista_quadro_2()
        self.root.mainloop()

    def tela(self):
        self.root.geometry("720x640")
        self.root.title("Gerenciador de Restaurante")
        self.root.configure(background='#005089')
        self.root.resizable(True, True)
        self.root.wm_maxsize(1080,720)
        self.root.wm_minsize(640,480)

    def quadros(self):
        self.quadro_1 = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_1.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.4)

        self.quadro_2 = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_2.place(relx=0.03, rely=0.48, relwidth=0.94, relheight=0.49)

    def botoes(self):
        self.bt_limpar = Button(self.quadro_1, text='Limpar', width=7,command=self.clear_entry)
        self.bt_limpar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*1 + ALTURA_BT*0, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_selecionar = Button(self.quadro_1, text='Selecionar', width=7)
        self.bt_selecionar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*2 + ALTURA_BT*1, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_buscar = Button(self.quadro_1, text='Buscar', width=7)
        self.bt_buscar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*3 + ALTURA_BT*2, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_adicionar = Button(self.quadro_1, background="#32CD32", text='Adicionar', width=7,command=self.insert_func)
        self.bt_adicionar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*4 + ALTURA_BT*3, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_editar = Button(self.quadro_1, background="#FFA500", text='Editar', width=7)
        self.bt_editar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*5 + ALTURA_BT*4, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_deletar = Button(self.quadro_1, background="#FF0000", text='Deletar', width=7,command=self.delete_func)
        self.bt_deletar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*6 + ALTURA_BT*5, relwidth=LARGURA_BT, relheight=ALTURA_BT)

    def label_entry(self):
        #           lABEL DO CADASTRO DE FUNCIONÁRIOS
        self.func_Id_Label = Label(self.quadro_1,text="ID_Funcionário",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Id_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Nome_Label = Label(self.quadro_1,text="Nome",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Nome_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Cargo_Label = Label(self.quadro_1,text="Cargo",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Cargo_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*3 + ALTURA_LABEL*2, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Salario_Label = Label(self.quadro_1,text="Salário",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Salario_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*4 + ALTURA_LABEL*3, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)
        
        
        #           ENTRY DOS FUNCIONÁRIOS
        self.func_Id_Entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.func_Id_Entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=0.1, relheight=ALTURA_LABEL)

        self.func_Nome_Entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.func_Nome_Entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=0.6, relheight=ALTURA_LABEL)

        self.func_Cargo_Entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.func_Cargo_Entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*3 + ALTURA_LABEL*2, relwidth=0.4, relheight=ALTURA_LABEL)

        self.func_Salario_Entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.func_Salario_Entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*4 + ALTURA_LABEL*3, relwidth=0.4, relheight=ALTURA_LABEL)
 
    def lista_quadro_2(self):
        self.lista = ttk.Treeview(self.quadro_2,height=3,columns=("col1","col2","col3","col4"))
        #self.lista.heading("#0",text="")
        self.lista.heading("#0",text="Id_Funcionário")
        self.lista.heading("#1",text="Nome")
        self.lista.heading("#2",text="Cargo")
        self.lista.heading("#3",text="Salário")

        #self.lista.column("#0",width=1)
        self.lista.column("#0",width=100)
        self.lista.column("#1",width=240)
        self.lista.column("#2",width=150)
        self.lista.column("#3",width=150)

        self.lista.place(relx=0.0,rely=0.0,relwidth=0.97,relheight=1)
        self.bar_rol = Scrollbar(self.quadro_2,orient='vertical')
        self.lista.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.97,rely=0.0,relwidth=0.03,relheight=1)
        



#janela principal
Application()
