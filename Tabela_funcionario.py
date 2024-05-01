from tkinter import *
from tkinter import ttk
import tkinter as tk
from Validadores import *
from Funcoes_sql import *

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

class Tabela_funcionario():

    def __init__(self,CONEX_DADOS,NOME_TABELA,NOME_COLUNA):

        self.CONEX_DADOS = CONEX_DADOS
        self.NOME_TABELA = NOME_TABELA
        self.NOME_COLUNA = NOME_COLUNA

        self.root = tk.Tk()
        self.fsql = Funcoes_sql(self.CONEX_DADOS,self.NOME_TABELA,self.NOME_COLUNA)
        self.verifica = Validadores()
        self.tela()
        self.quadros()
        self.botoes()
        self.label_entry()
        self.lista_quadro_2()
        self.atualiza_tabela()
        self.root.mainloop()
    
    def tela(self):
        self.root.geometry("720x640")
        self.root.title(self.NOME_TABELA)
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
        self.col0_Label = Label(self.quadro_1,text=self.NOME_COLUNA[0],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.col0_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.col1_Label = Label(self.quadro_1,text=self.NOME_COLUNA[1],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.col1_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.col2_Label = Label(self.quadro_1,text=self.NOME_COLUNA[2],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.col2_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*3 + ALTURA_LABEL*2, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)

        self.col3_Label = Label(self.quadro_1,text=self.NOME_COLUNA[3],font=('Arial',12),bg="#feffff", fg="#403d3d")
        self.col3_Label.place(relx=X_LABEL, rely=ESPACAMENTO_LB*4 + ALTURA_LABEL*3, relwidth=LARGURA_LABEL, relheight=ALTURA_LABEL)
        
        
        #           ENTRY DOS FUNCIONÁRIOS
        self.col0_entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.col0_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*1 + ALTURA_LABEL*0, relwidth=0.6, relheight=ALTURA_LABEL)

        self.col1_entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.col1_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*2 + ALTURA_LABEL*1, relwidth=0.6, relheight=ALTURA_LABEL)

        self.col2_entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.col2_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*3 + ALTURA_LABEL*2, relwidth=0.4, relheight=ALTURA_LABEL)

        self.col3_entry = Entry(self.quadro_1, width=25, justify='left', font=("Arial", 12), highlightthickness=1, relief="solid")
        self.col3_entry.place(relx=X_LABEL+LARGURA_LABEL, rely=ESPACAMENTO_LB*4 + ALTURA_LABEL*3, relwidth=0.4, relheight=ALTURA_LABEL)

    def lista_quadro_2(self):
        self.lista = ttk.Treeview(self.quadro_2, height=3, columns=self.NOME_COLUNA)
        
        # Adiciona as colunas com os nomes fornecidos
        self.lista.heading("#0",text="")
        for idx, nome_coluna in enumerate(self.NOME_COLUNA):
            self.lista.heading(f"#{idx+1}", text=nome_coluna)

        # Configuração das colunas
        width_column = int(500/len(self.NOME_COLUNA))
        self.lista.column("#0",width=0, stretch=False)
        for idx in range(len(self.NOME_COLUNA)):
            self.lista.column(f"#{idx+1}", width=width_column, stretch=True)

        self.lista.place(relx=0.0,rely=0.0,relwidth=0.97,relheight=1)
        self.bar_rol = Scrollbar(self.quadro_2,orient='vertical')
        self.lista.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.97,rely=0.0,relwidth=0.03,relheight=1)
        self.lista.bind("<Double-1>", self.preencher)

    # ------ FUNÇÕES AUXILIARES DO FRONT -------
    def get_entry(self):
        return[self.col0_entry.get()+"", #STT-01
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

        for array in self.fsql.get_data():
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
        if not self.fsql.insert_funcionario(entrys): return
        self.atualiza_tabela()
        self.clear_entry()

    def update_bt(self):
        entrys = self.get_entry()
        if not self.fsql.update_funcionario(entrys): return
        self.atualiza_tabela()
        self.clear_entry()
    
    def delete_bt(self):
        entrys = self.get_entry()
        if not self.fsql.delete_funcionario(entrys): return
        self.atualiza_tabela()
        self.clear_entry()

    def select_bt(self):
        entrys = self.get_entry()
        
        if self.verifica.espaco_vazio(entrys) == 4:
            self.atualiza_tabela()
            return
        
        encontrado = self.fsql.select_funcionario(entrys)
        if encontrado is False: return
        self.mostra_tabela(encontrado)
        self.clear_entry()