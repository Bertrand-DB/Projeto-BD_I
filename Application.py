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

    def get_data(self):
            self.conexao()
            self.cursor.execute(f"SELECT * FROM {TABELA[0]}")
            data = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            return data

    def atualiza_tabela(self):
        for data in self.lista.get_children():
            self.lista.delete(data)

        for array in self.get_data():
            self.lista.insert("", END,iid=array, text="", values=(array))

    def get_entry(self):
        self.e_id = self.func_Id_Entry.get()
        self.e_nome = self.func_Nome_Entry.get()
        self.e_cargo = self.func_Cargo_Entry.get()
        self.e_salario = self.func_Salario_Entry.get().replace(',','.')     #sintaxe do sql usa apenas '.'

    def insert_func(self):
        self.get_entry()
        
        if self.e_id != "":     #banco de dados que define os id únicos
            messagebox.showinfo("Ops, entrada inválida", f"Deixa que eu cuido de {TABELA[1]}")
        self.e_id = None

        if self.e_nome.strip() == "" or self.e_cargo.strip() == "" or self.e_salario.strip() == "":     #os campos não podem ser vazios ou só espaços
            messagebox.showerror("Erro!", "Por favor, preencha os espaços vazios!")
            return
        
        try:
            int(self.e_nome)
        except:
            self.e_nome     #caso não dê para converter, quer dizer que o nome não é um número, e não precisa fazer nada
        else:               
            messagebox.showerror("ERRO! - Elon Musk", f"'{TABELA[2]}' precisa ser um nome!")
            return

        self.conexao()
        self.consulta =f"INSERT INTO {TABELA[0]} ({TABELA[1]},{TABELA[2]},{TABELA[3]},{TABELA[4]})VALUES"+"(%s,%s,%s,%s)"
        self.valores=(self.e_id, self.e_nome,self.e_cargo,self.e_salario)
        
        try:
            self.cursor.execute(self.consulta,self.valores)
        except mysql.connector.errors.IntegrityError as integrity_error:      #previne erros como nomes(unique key) duplicados 
            messagebox.showerror(f"ERRO! - {integrity_error.errno}", integrity_error.msg)
            self.conn.close()
            return

        self.conn.commit()
        self.conn.close()
        self.atualiza_tabela()
        self.clear_entry()

    def delete_func(self):
        self.get_entry()

        try:
            self.e_id = int(self.e_id)
        except ValueError as val_error:
            messagebox.showerror(f"ERRO! - Valor inválido", f"'{TABELA[1]}' a ser deletado precisa ser um valor válido!")
            return

        self.conexao()
        self.consulta = f"DELETE FROM {TABELA[0]} WHERE {TABELA[1]} = "+"%s"
        self.valores = [self.e_id]
        self.cursor.execute(self.consulta,self.valores)
        self.conn.commit()
        self.conn.close()
        self.atualiza_tabela()
        self.clear_entry()

    def select_func(self, event):
        self.clear_entry()
        self.lista.selection()
        
        for n in self.lista.selection():
            col1, col2, col3, col4 = self.lista.item(n, 'values')
            self.func_Id_Entry.insert(END, col1)
            self.func_Nome_Entry.insert(END, col2)
            self.func_Cargo_Entry.insert(END, col3)
            self.func_Salario_Entry.insert(END, col4)
    
    def update_func(self):
        self.get_entry()
        self.conexao()
        self.consulta = f"UPDATE {TABELA[0]} SET {TABELA[2]} = "+"%s"+f", {TABELA[3]} = "+"%s"+f", {TABELA[4]} = "+"%s"+f" WHERE {TABELA[1]} = "+"%s" #é feio, mas funciona kkk
        self.valores = (self.e_nome, self.e_cargo, self.e_salario, self.e_id)

        try:
            self.cursor.execute(self.consulta,self.valores)
        except mysql.connector.errors.IntegrityError as integrity_error:    #previne erros como um nome duplicado
            messagebox.showerror(f"ERRO! - {integrity_error.errno}", integrity_error.msg)
            self.conn.close()
            return

        self.conn.commit()
        self.conn.close()
        self.atualiza_tabela()
        self.clear_entry()

    def busca_func(self):
        self.get_entry()

        if self.e_id == "" and self.e_nome == "" and self.e_cargo == "" and self.e_salario == "":              #retorna a tabela completa
            self.atualiza_tabela()
            return
        elif self.e_id != "" and self.e_nome == "" and self.e_cargo == "" and self.e_salario == "":            #busca por id
            self.consulta = f"SELECT * FROM {TABELA[0]} WHERE {TABELA[1]} LIKE "+"%s"+f" ORDER BY {TABELA[1]} ASC"
            self.e_id += '%'                                                                                   # o % permite a busca por resultados que comecem com o valor precedido
            self.valores = [self.e_id]

        elif self.e_id == "" and self.e_nome != "" and self.e_cargo == "" and self.e_salario == "":            #busca por nome
            self.consulta = f"SELECT * FROM {TABELA[0]} WHERE {TABELA[2]} LIKE "+"%s"+f" ORDER BY {TABELA[2]} ASC"
            self.e_nome += '%'
            self.valores = [self.e_nome]

        elif self.e_id == "" and self.e_nome == "" and self.e_cargo != "" and self.e_salario == "":            #busca por cargo
            self.consulta = f"SELECT * FROM {TABELA[0]} WHERE {TABELA[3]} LIKE "+"%s"+f" ORDER BY {TABELA[3]} ASC"
            self.e_cargo += '%'
            self.valores = [self.e_cargo]

        elif self.e_id == "" and self.e_nome == "" and self.e_cargo == "" and self.e_salario != "":            #busca por salário
            self.consulta = f"SELECT * FROM {TABELA[0]} WHERE {TABELA[4]} LIKE "+"%s"+f" ORDER BY {TABELA[4]} ASC"
            self.e_salario += '%'
            self.valores = [self.e_salario]

        else:
            messagebox.showerror("ERRO! - Múltipla entrada", "Preencha apenas UMA entrada para a busca!")
            self.clear_entry()
            return
            
        self.conexao()
        self.cursor.execute(self.consulta, self.valores)
        encontrado = self.cursor.fetchall()
        
        self.lista.delete(*self.lista.get_children())
        for i in encontrado:
            self.lista.insert("", END, values=i)
        self.clear_entry()
        self.conn.close()


class Application(funcoes):

    def __init__(self):
        self.root = tk.Tk()
        self.tela()
        self.quadros()
        self.botoes()
        self.label_entry()
        self.lista_quadro_2()
        self.atualiza_tabela()
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
        
        self.bt_buscar = Button(self.quadro_1, text='Buscar', width=7, command=self.busca_func)
        self.bt_buscar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*2 + ALTURA_BT*1, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_adicionar = Button(self.quadro_1, background="#32CD32", text='Adicionar', width=7,command=self.insert_func)
        self.bt_adicionar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*3 + ALTURA_BT*2, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_editar = Button(self.quadro_1, background="#FFA500", text='Editar', width=7, command=self.update_func)
        self.bt_editar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*4 + ALTURA_BT*3, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_deletar = Button(self.quadro_1, background="#FF0000", text='Deletar', width=7,command=self.delete_func)
        self.bt_deletar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*5 + ALTURA_BT*4, relwidth=LARGURA_BT, relheight=ALTURA_BT)

    def label_entry(self):
        #           lABEL DO CADASTRO DE FUNCIONÁRIOS
        self.func_Id_Label = Label(self.quadro_1,text=TABELA[1],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Id_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Nome_Label = Label(self.quadro_1,text=TABELA[2],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Nome_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Cargo_Label = Label(self.quadro_1,text=TABELA[3],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Cargo_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*3 + ALTURA_LABEL*2, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Salario_Label = Label(self.quadro_1,text=TABELA[4],font=('Arial',12),bg="#feffff", fg="#403d3d")
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
        
        self.lista.heading("#0",text="")
        self.lista.heading("#1",text=TABELA[1])
        self.lista.heading("#2",text=TABELA[2])
        self.lista.heading("#3",text=TABELA[3])
        self.lista.heading("#4",text=TABELA[4])

        self.lista.column("#0",width=0, stretch=False)
        self.lista.column("#1",width=50)
        self.lista.column("#2",width=200)
        self.lista.column("#3",width=125)
        self.lista.column("#4",width=125)

        self.lista.place(relx=0.0,rely=0.0,relwidth=0.97,relheight=1)
        self.bar_rol = Scrollbar(self.quadro_2,orient='vertical')
        self.lista.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.97,rely=0.0,relwidth=0.03,relheight=1)
        self.lista.bind("<Double-1>", self.select_func)
    
    
        

#janela principal
Application()
