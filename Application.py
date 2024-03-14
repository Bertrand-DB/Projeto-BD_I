import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

#Nome da tabela e colunas
NOME_TABELA = "Funcionários"
NOME_COLUNA = ["Id_Funcionários", "Nome", "Cargo", "Salário"]

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


    # FUNÇÕES AUXILIARES PARA TRATAMENTO DE ENTRADA
class verifica():

    def espaco_vazio(self, entradas):   #verifica se a(s) entradas possuem apenas espaço ou são vazias
        vazios = False
        for i in entradas:
            i = str(i)
            if i.strip() == "":
                vazios += 1
        return vazios
    
    def tem_numero(self, entradas):     #verifica se a(s) entradas possuem ao menos um caracter numero
        numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for palavra in entradas:
            for num in numeros:
                if palavra.find(num) != -1:
                    return True
        return False

    def so_numero(self, entradas):            #verifica se a entrada é um número em forma de string, int ou float
        try:        
            if type(entradas) is list:
                for palavra in entradas:
                    float(palavra)
            else:
                float(entradas) 

        except ValueError:
            return False

        return True   

    # ------ OPERAÇÕES DO SQL ------------------
class funcoes_sql(verifica):

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
            self.cursor.execute(f"SELECT * FROM {NOME_TABELA}")
            data = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            return data

    def entry_ok(self, op, entrys):

        if self.tem_numero([entrys[1],entrys[2]]):            
            messagebox.showerror("ERRO!", f"'{NOME_COLUNA[1]}' e '{NOME_COLUNA[2]}' não pode ser um número!")
            return  False
        
        if op == "select":
            if self.espaco_vazio(entrys) <= 2:
                messagebox.showerror("ERRO! - Múltipla entrada", "Preencha apenas UMA entrada para a busca!")
                return False
            return True

        if self.espaco_vazio([entrys[1],entrys[2],entrys[3]]):
            messagebox.showerror("Erro!", "Por favor, preencha os espaços vazios!")
            return False
        
        
        if not self.so_numero(entrys[3]):
            messagebox.showerror("ERRO!", f"'{NOME_COLUNA[3]}' precisa ser um número!")
            return False
        
        if float(entrys[3]) > 99999.99:
            messagebox.showerror("ERRO!", f"'{NOME_COLUNA[3]}' não deve ser maior que R$99.999,99")
            return False
        
        if op == "insert":
            if not self.espaco_vazio(entrys[0]):
                messagebox.showinfo("Ops, entrada inválida", f"Deixa que eu cuido de {NOME_COLUNA[0]}")
        
        elif op == "delete":
            if not self.so_numero(entrys[0]):
                messagebox.showerror("ERRO!", f"'{NOME_COLUNA[0]}' precisa ser um número!")
                return False
        
        elif op == "update":
            if not self.so_numero(entrys[0]):
                messagebox.showerror("ERRO!", f"'{NOME_COLUNA[0]}' precisa ser um número!")
                return False

        return True

    def insert(self, entrys):
        if not self.entry_ok("insert", entrys): return False
        
        self.conexao()
        self.consulta =f"INSERT INTO {NOME_TABELA} ({NOME_COLUNA[0]},{NOME_COLUNA[1]},{NOME_COLUNA[2]},{NOME_COLUNA[3]})VALUES"+"(%s,%s,%s,%s)"
        self.valores=(None, entrys[1], entrys[2], entrys[3])
        
        try:
            self.cursor.execute(self.consulta,self.valores)
        except mysql.connector.errors.IntegrityError:      #previne erros como nomes(unique key) duplicados 
            messagebox.showerror(f"ERRO!", f"O {NOME_COLUNA[1]} '{entrys[1]}' já existe")
            self.conn.close()
            return False

        self.conn.commit()
        self.conn.close()
        return True

    def delete(self, entrys):
        if not self.entry_ok("delete", entrys): return False

        self.conexao()
        self.consulta = f"DELETE FROM {NOME_TABELA} WHERE {NOME_COLUNA[0]} = "+"%s"
        self.valores = [entrys[0]]
        self.cursor.execute(self.consulta,self.valores)
        self.conn.commit()
        self.conn.close()
        return True

    def update(self, entrys):
        if not self.entry_ok("update", entrys): return False

        self.conexao()
        self.consulta = f"UPDATE {NOME_TABELA} SET {NOME_COLUNA[1]} = "+"%s"+f", {NOME_COLUNA[2]} = "+"%s"+f", {NOME_COLUNA[3]} = "+"%s"+f" WHERE {NOME_COLUNA[0]} = "+"%s" #é feio, mas funciona kkk
        self.valores = (entrys[1], entrys[2], entrys[3], entrys[0])

        try:
            self.cursor.execute(self.consulta,self.valores)
        except mysql.connector.errors.IntegrityError as integrity_error:    #previne erros como um nome duplicado
            messagebox.showerror(f"ERRO! - {integrity_error.errno}", integrity_error.msg)
            self.conn.close()
            return

        self.conn.commit()
        self.conn.close()
        return True

    def select(self, entrys):

        if not self.entry_ok("select",entrys): return False
        entrys[0] = entrys[0].strip()

        if entrys[0] != "" and entrys[1] == "" and entrys[2] == "" and entrys[3] == "":            #busca por id
            print("Apenas ID - "+str(self.espaco_vazio(entrys[0])))
            self.consulta = f"SELECT * FROM {NOME_TABELA} WHERE {NOME_COLUNA[0]} LIKE "+"%s"+f" ORDER BY {NOME_COLUNA[0]} ASC"
            entrys[0] += '%'                                                                                   # o % permite a busca por resultados que comecem com o valor precedido
            self.valores = [entrys[0]]

        elif entrys[0] == "" and entrys[1] != "" and entrys[2] == "" and entrys[3] == "":            #busca por nome
            print("Apenas Nome - "+str(self.espaco_vazio(entrys[1])))
            self.consulta = f"SELECT * FROM {NOME_TABELA} WHERE {NOME_COLUNA[1]} LIKE "+"%s"+f" ORDER BY {NOME_COLUNA[1]} ASC"
            entrys[1] += '%'
            self.valores = [entrys[1]]

        elif entrys[0] == "" and entrys[1] == "" and entrys[2] != "" and entrys[3] == "":            #busca por cargo
            print("Apenas Cargo - "+str(self.espaco_vazio(entrys[2])))
            self.consulta = f"SELECT * FROM {NOME_TABELA} WHERE {NOME_COLUNA[2]} LIKE "+"%s"+f" ORDER BY {NOME_COLUNA[2]} ASC"
            entrys[2] += '%'
            self.valores = [entrys[2]]

        elif entrys[0] == "" and entrys[1] == "" and entrys[2] == "" and entrys[3] != "":            #busca por salário
            print("Apenas Salário - "+str(self.espaco_vazio(entrys[3])))
            self.consulta = f"SELECT * FROM {NOME_TABELA} WHERE {NOME_COLUNA[3]} LIKE "+"%s"+f" ORDER BY {NOME_COLUNA[3]} ASC"
            entrys[3] += '%'
            self.valores = [entrys[3]]
            
        self.conexao()
        self.cursor.execute(self.consulta, self.valores)
        encontrado = self.cursor.fetchall()
        self.conn.close()

        return encontrado
        
    # ------ FRONT -----------------------------
class Application(funcoes_sql):

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
        
        self.bt_buscar = Button(self.quadro_1, text='Buscar', width=7, command=self.select_bt)
        self.bt_buscar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*2 + ALTURA_BT*1, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_adicionar = Button(self.quadro_1, background="#32CD32", text='Adicionar', width=7,command=self.insert_bt)
        self.bt_adicionar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*3 + ALTURA_BT*2, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_editar = Button(self.quadro_1, background="#FFA500", text='Editar', width=7, command=self.update_bt)
        self.bt_editar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*4 + ALTURA_BT*3, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_deletar = Button(self.quadro_1, background="#FF0000", text='Deletar', width=7,command=self.delete_bt)
        self.bt_deletar.place(relx=X_BOTAO, rely=ESPACAMENTO_BT*5 + ALTURA_BT*4, relwidth=LARGURA_BT, relheight=ALTURA_BT)

    def label_entry(self):
        #           lABEL DO CADASTRO DE FUNCIONÁRIOS
        self.func_Id_Label = Label(self.quadro_1,text=NOME_COLUNA[0],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Id_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Nome_Label = Label(self.quadro_1,text=NOME_COLUNA[1],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Nome_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Cargo_Label = Label(self.quadro_1,text=NOME_COLUNA[2],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Cargo_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*3 + ALTURA_LABEL*2, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.func_Salario_Label = Label(self.quadro_1,text=NOME_COLUNA[3],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.func_Salario_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*4 + ALTURA_LABEL*3, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)
        
        
        #           ENTRY DOS FUNCIONÁRIOS
        self.col0_entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.col0_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=0.1, relheight=ALTURA_LABEL)

        self.col1_entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.col1_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=0.6, relheight=ALTURA_LABEL)

        self.col2_entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.col2_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*3 + ALTURA_LABEL*2, relwidth=0.4, relheight=ALTURA_LABEL)

        self.col3_entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.col3_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*4 + ALTURA_LABEL*3, relwidth=0.4, relheight=ALTURA_LABEL)

    def lista_quadro_2(self):
        self.lista = ttk.Treeview(self.quadro_2,height=3,columns=("col1","col2","col3","col4"))
        
        self.lista.heading("#0",text="")
        self.lista.heading("#1",text=NOME_COLUNA[0])
        self.lista.heading("#2",text=NOME_COLUNA[1])
        self.lista.heading("#3",text=NOME_COLUNA[2])
        self.lista.heading("#4",text=NOME_COLUNA[3])

        self.lista.column("#0",width=0, stretch=False)
        self.lista.column("#1",width=50)
        self.lista.column("#2",width=200)
        self.lista.column("#3",width=125)
        self.lista.column("#4",width=125)

        self.lista.place(relx=0.0,rely=0.0,relwidth=0.97,relheight=1)
        self.bar_rol = Scrollbar(self.quadro_2,orient='vertical')
        self.lista.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.97,rely=0.0,relwidth=0.03,relheight=1)
        self.lista.bind("<Double-1>", self.preencher)

    # ------ FUNÇÕES AUXILIARES DO FRONT -------
    def get_entry(self):
        return[self.col0_entry.get()+" ", 
               self.col1_entry.get().strip(), 
               self.col2_entry.get().strip(), 
               self.col3_entry.get().replace(',','.')]
    
    def preencher(self, event):
        self.clear_entry()
        self.lista.selection()
        
        for n in self.lista.selection():
            col1, col2, col3, col4 = self.lista.item(n, 'values')
            self.col0_entry.insert(END, col1)
            self.col1_entry.insert(END, col2)
            self.col2_entry.insert(END, col3)
            self.col3_entry.insert(END, col4)
        
    def atualiza_tabela(self):
        for data in self.lista.get_children():
            self.lista.delete(data)

        for array in self.get_data():
            self.lista.insert("", END,iid=array, text="", values=(array))

    def mostra_tabela(self, dados):
        for data in self.lista.get_children():
            self.lista.delete(data)

        for array in dados:
            self.lista.insert("", END,iid=array, text="", values=(array))

    def clear_entry(self):
        self.col0_entry.delete(0,END)
        self.col1_entry.delete(0,END)
        self.col2_entry.delete(0,END)
        self.col3_entry.delete(0,END)
    
    # ------ FUNÇÕES DOS BOTÕES ----------------
    def insert_bt(self):
        entrys = self.get_entry()
        if not self.insert(entrys): return
        self.atualiza_tabela()
        self.clear_entry()

    def update_bt(self):
        entrys = self.get_entry()
        if not self.update(entrys): return
        self.atualiza_tabela()
        self.clear_entry()
    
    def delete_bt(self):
        entrys = self.get_entry()
        if not self.delete(entrys): return
        self.atualiza_tabela()
        self.clear_entry()

    def select_bt(self):
        entrys = self.get_entry()
        
        if self.espaco_vazio(entrys) == 4:
            self.atualiza_tabela()
            return
        
        encontrado = self.select(entrys)
        if encontrado is False: return
        self.mostra_tabela(encontrado)
        self.clear_entry()

    
#janela principal
Application()
