import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk


class funcoes():
    
    def clear_entry(self):
        self.func_Id_Entry.delete(0,END)
        self.func_Nome_Entry.delete(0,END)
        self.func_Cargo_Entry.delete(0,END)
        self.func_Salario_Entry.delete(0,END)

    def conexao(self):
        self.conexao = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            password="746832fC",
            database="teste"
        )
        self.cursor= self.conexao.cursor()

    def insert_func(self):
        self.func_Id = self.func_Id_Entry.get()
        self.func_Nome = self.func_Nome_Entry.get()
        self.func_Cargo = self.func_Cargo_Entry.get()
        self.func_Salario = self.func_Salario_Entry.get()
        self.conexao()
        self.consulta ="INSERT INTO cadastro (id,nome,cargo,salario)VALUES(%s,%s,%s,%s)"
        self.valores=(self.func_Id,self.func_Nome,self.func_Cargo,self.func_Salario)
        self.cursor.execute(self.consulta,self.valores)
        self.conexao.commit()
        self.conexao.close()

    def delete_func(self):
        self.func_delete = self.func_Nome_Entry.get()
        self.conexao()
        self.consulta = "DELETE FROM cadastro WHERE nome = %s "
        self.valores = [self.func_delete]
        self.cursor.execute(self.consulta,self.valores)
        self.conexao.commit()
        self.conexao.close()

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
        self.root.resizable(False, False)
        self.root.wm_maxsize(1188,792)
        self.root.wm_minsize(640,480)

    def quadros(self):
        self.quadro_1 = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_1.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.4)

        self.quadro_2 = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_2.place(relx=0.03, rely=0.48, relwidth=0.94, relheight=0.49)

    def botoes(self):
        self.bt_limpar = Button(self.quadro_1, text='Limpar', width=7,command=self.clear_entry)
        self.bt_limpar.grid(row=3,column=3, columnspan=1,padx=10,pady=5)
        
        self.bt_selecionar = Button(self.quadro_1, text='Selecionar', width=7)
        self.bt_selecionar.grid(row=4,column=3,columnspan=1,padx=10,pady=5)
        
        self.bt_buscar = Button(self.quadro_1, text='Buscar', width=7)
        self.bt_buscar.grid(row=5,column=3,columnspan=1,padx=10,pady=5)

        self.bt_adicionar = Button(self.quadro_1, background="#32CD32", text='Adicionar', width=7,command=self.insert_func)
        self.bt_adicionar.grid(row=3,column=4,columnspan=1,padx=10,pady=5)
        
 
        self.bt_editar = Button(self.quadro_1, background="#FFA500", text='Editar', width=7)
        self.bt_editar.grid(row=4,column=4,columnspan=1,padx=10,pady=5)

        self.bt_deletar = Button(self.quadro_1, background="#FF0000", text='Deletar', width=7,command=self.delete_func)
        self.bt_deletar.grid(row=5,column=4,columnspan=1,padx=10,pady=5)

    def label_entry(self):
        #           lABEL DO CADASTRO DE FUNCIONÁRIOS
        self.func_Id_Label = Label(self.quadro_1,text="ID Funcionário",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Id_Label.grid(row=3,column=0,columnspan=1,padx=0,pady=5)

        self.func_Nome_Label = Label(self.quadro_1,text="Nome",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Nome_Label.grid(row=4,column=0,columnspan=1,padx=0,pady=5)

        self.func_Cargo_Label = Label(self.quadro_1,text="Cargo",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Cargo_Label.grid(row=5,column=0,columnspan=1,padx=0,pady=5)

        self.func_Salario_Label = Label(self.quadro_1,text="Salário",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Salario_Label.grid(row=6,column=0,columnspan=1,padx=0,pady=5)
        
        
        #           ENTRY DOS FUNCIONÁRIOS
        self.func_Id_Entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.func_Id_Entry.grid(row=3,column=1,columnspan=1,padx=0,pady=5)

        self.func_Nome_Entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.func_Nome_Entry.grid(row=4,column=1,columnspan=1,padx=0,pady=5)

        self.func_Cargo_Entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.func_Cargo_Entry.grid(row=5,column=1,columnspan=1,padx=0,pady=5)

        self.func_Salario_Entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.func_Salario_Entry.grid(row=6,column=1,columnspan=1,padx=0,pady=5)

    
    def lista_quadro_2(self):
        self.lista = ttk.Treeview(self.quadro_2,height=3,columns=("col1","col2","col3","col4"))
        self.lista.heading("#0",text="")
        self.lista.heading("#1",text="Id")
        self.lista.heading("#2",text="Nome")
        self.lista.heading("#3",text="Cargo")
        self.lista.heading("#4",text="Salário")

        self.lista.column("#0",width=1)
        self.lista.column("#1",width=50)
        self.lista.column("#2",width=200)
        self.lista.column("#3",width=125)
        self.lista.column("#4",width=125)

        self.lista.place(relx=0.01,rely=0.1,relwidth=0.95,relheight=0.85)
        self.bar_rol = Scrollbar(self.quadro_2,orient='vertical')
        self.lista.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.96,rely=0.1,relwidth=0.02,relheight=0.85)
        



#janela principal
Application()
