from tkinter import *
from tkinter import ttk
import tkinter as tk
from Verificadores import *
from Funcoes_sql import *

#constantes de posição dos botões
LARGURA_BT = 0.12
ALTURA_BT = 0.14
ESPACAMENTO_BT = 0.02
X_BOTAO = 1 - LARGURA_BT - ESPACAMENTO_BT

#constantes de posição das labels e entrys
ESPACAMENTO_LB = 0.08
LARGURA_LABEL = 0.18
ALTURA_LABEL = 0.2
X_LABEL = 0.04

class Navegacao():

    def __init__(self,CONEX_DADOS,NOME_TABELA,NOME_COLUNA):

        self.CONEX_DADOS = CONEX_DADOS
        self.NOME_TABELA = NOME_TABELA
        self.NOME_COLUNA = NOME_COLUNA

        self.root = tk.Tk()
        self.fsql = Funcoes_sql(self.CONEX_DADOS,self.NOME_TABELA,self.NOME_COLUNA)
        self.verifica = Verificadores()
        self.tela()
        self.quadros()
        self.botoes()
        self.label_entry()
        self.lista_inferior()
        self.atualiza_tabela()
        self.root.mainloop()
    
    def tela(self):
        self.root.geometry("720x640")
        self.root.title("Restaurante Chapéu de Palha")
        self.root.configure(background='#005089')
        self.root.resizable(True, True)
        self.root.wm_maxsize(1080,720)
        self.root.wm_minsize(640,480)

    def quadros(self):
        self.quadro_login = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_login.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.25)

        self.quadro_lista = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_lista.place(relx=0.03, rely=0.33, relwidth=0.94, relheight=0.64)

    def botoes(self):
        self.bt_limpar = Button(self.quadro_login, text='Entrar', width=7)
        self.bt_limpar.place(relx=0.225, rely=0.75, relwidth=0.25, relheight=0.2)
        
        self.bt_buscar = Button(self.quadro_login, text='Registre-se', width=7)
        self.bt_buscar.place(relx=0.525, rely=0.75, relwidth=0.25, relheight=0.2)

    def label_entry(self):
        #-----------LABELS
        self.id_Label = Label(self.quadro_login,text="Id",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.id_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.nome_Label = Label(self.quadro_login,text="Nome",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.nome_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)
        
        #-----------ENTRYS
        self.id_entry = Entry(self.quadro_login, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.id_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=0.1, relheight=ALTURA_LABEL)

        self.nome_entry = Entry(self.quadro_login, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.nome_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=0.6, relheight=ALTURA_LABEL)

    def lista_inferior(self):
        self.lista = ttk.Treeview(self.quadro_lista,height=3,columns=("col1","col2","col3","col4"))
        
        self.lista.heading("#0",text="")
        self.lista.heading("#1",text=self.NOME_COLUNA[0])
        self.lista.heading("#2",text=self.NOME_COLUNA[1])
        self.lista.heading("#3",text=self.NOME_COLUNA[2])
        self.lista.heading("#4",text=self.NOME_COLUNA[3])

        self.lista.column("#0",width=0, stretch=False)
        self.lista.column("#1",width=50)
        self.lista.column("#2",width=200)
        self.lista.column("#3",width=125)
        self.lista.column("#4",width=125)

        self.lista.place(relx=0.0,rely=0.0,relwidth=0.97,relheight=1)
        self.bar_rol = Scrollbar(self.quadro_lista,orient='vertical')
        self.lista.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.97,rely=0.0,relwidth=0.03,relheight=1)

    # ------ FUNÇÕES AUXILIARES DO FRONT -------
    def get_entry(self):
        return[self.col0_entry.get()+" ",
               self.col1_entry.get().strip()]
    
    def atualiza_tabela(self):
        for data in self.lista.get_children():
            self.lista.delete(data)

        for array in self.fsql.get_data():
            self.lista.insert("", END,iid=array, text="", values=(array))

    # ------ FUNÇÕES DOS BOTÕES ----------------
    def entrar_bt(self):
        entrys = self.get_entry()
        

    def registrese_bt(self):
        entrys = self.get_entry()
        
class Navegacao_cli():
    def __init__(self,CONEX_DADOS,NOME_TABELA,NOME_COLUNA):

        self.CONEX_DADOS = CONEX_DADOS
        self.NOME_TABELA = NOME_TABELA
        self.NOME_COLUNA = NOME_COLUNA

        self.root = tk.Tk()
        self.fsql = Funcoes_sql(self.CONEX_DADOS,self.NOME_TABELA,self.NOME_COLUNA)
        self.verifica = Verificadores()
        self.tela()
        self.quadros()
        self.abas()
        self.botoes()
        self.label_entry()
        self.lista_inferior()
        self.atualiza_tabela()
        self.root.mainloop()
    
    def tela(self):
        self.root.geometry("720x640")
        self.root.title("Restaurante Chapéu de Palha")
        self.root.configure(background='#005089')
        self.root.resizable(True, True)
        self.root.wm_maxsize(1080,720)
        self.root.wm_minsize(640,480)

    def quadros(self):
        self.quadro_login = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_login.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.4)

        self.quadro_lista = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_lista.place(relx=0.03, rely=0.48, relwidth=0.94, relheight=0.49)

    def abas(self):
        self.aba = ttk.Notebook(self.quadro_login)
        
        self.aba_compra = Frame(self.aba)
        self.aba_compra.configure(background='lightgray')
        
        self.aba_info = Frame(self.aba)
        self.aba_info.configure(background= 'lightgray')

        self.aba.add(self.aba_compra, text= "Pedir")
        self.aba.add(self.aba_info, text= "Perfil")

        self.aba.place(relx=0, rely=0, relwidth=1, relheight=1)

    def botoes(self):
        self.bt_limpar = Button(self.quadro_login, text='Entrar', width=7)
        self.bt_limpar.place(relx=0.225, rely=0.75, relwidth=0.25, relheight=0.2)
        
        self.bt_buscar = Button(self.quadro_login, text='Registre-se', width=7)
        self.bt_buscar.place(relx=0.525, rely=0.75, relwidth=0.25, relheight=0.2)

    def label_entry(self):
        #-----------LABELS
        self.id_Label = Label(self.aba_compra,text="Id",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.id_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.nome_Label = Label(self.aba_compra,text="Nome",font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.nome_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)
        
        #-----------ENTRYS
        self.id_entry = Entry(self.aba_compra, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.id_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=0.1, relheight=ALTURA_LABEL)

        self.nome_entry = Entry(self.aba_compra, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.nome_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=0.6, relheight=ALTURA_LABEL)

    def lista_inferior(self):
        self.lista = ttk.Treeview(self.quadro_lista, height=3, columns=self.NOME_COLUNA)
        
        # Adiciona as colunas com os nomes fornecidos
        self.lista.heading("#0",text="")
        for idx, nome_coluna in enumerate(self.NOME_COLUNA):
            self.lista.heading(f"#{idx+1}", text=nome_coluna)

        # Configuração das colunas
        width_column = int(500/len(self.NOME_COLUNA))
        self.lista.column("#0",width=0, stretch=False)
        for idx in range(len(self.NOME_COLUNA)):
            self.lista.column(f"#{idx+1}", width=width_column, stretch=True)

        self.lista.place(relx=0.0, rely=0.0, relwidth=0.97, relheight=1)
        self.bar_rol = Scrollbar(self.quadro_lista, orient='vertical')
        self.lista.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.97, rely=0.0, relwidth=0.03, relheight=1)


    # ------ FUNÇÕES AUXILIARES DO FRONT -------
    def get_entry(self):
        return[self.id_entry.get()+" ",
               self.nome_entry.get().strip()]
    
    def atualiza_tabela(self):
        for data in self.lista.get_children():
            self.lista.delete(data)

        for array in self.fsql.get_data():
            self.lista.insert("", END,iid=array, text="", values=(array))

    # ------ FUNÇÕES DOS BOTÕES ----------------
    def entrar_bt(self):
        entrys = self.get_entry()
        

    def registrese_bt(self):
        entrys = self.get_entry()
