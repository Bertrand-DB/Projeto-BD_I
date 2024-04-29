from tkinter import *
from tkinter import ttk
import tkinter as tk
from Validadores import *
from Funcoes_sql import *
import re

#constantes de posição dos botões
LARGURA_BT = 0.10
ALTURA_BT = 0.14
ESPACAMENTO_BT = 0.02
X_BOTAO = 1 - LARGURA_BT - ESPACAMENTO_BT

#constantes de posição das labels e entrys



class Navegacao():
    def __init__(self,CONEX_DADOS,NOME_TABELA,NOME_COLUNA):

        self.CONEX_DADOS = CONEX_DADOS
        self.NOME_TABELA = NOME_TABELA
        self.NOME_COLUNA = NOME_COLUNA

        self.user_data = []

        self.root = tk.Tk()
        self.fsql = Funcoes_sql(self.CONEX_DADOS,self.NOME_TABELA,self.NOME_COLUNA)
        self.valida = Validadores()

        self.validar_digitos = self.root.register(self.valida.digitos)         #permite o tkinter reconhecer os validadores
        self.validar_ponto_dec = self.root.register(self.valida.ponto_decimal)
        self.validar_string = self.root.register(self.valida.string)

        self.tela()
        self.quadro_inf()
        self.quadro_login()
        self.atualiza_tabela()
        self.root.mainloop()
    
    def tela(self):
        self.root.geometry("1080x720")
        self.root.title("Restaurante Chapéu de Palha")
        self.root.configure(background='#005089')
        self.root.resizable(True, True)
        self.root.wm_maxsize(1620,1080)
        self.root.wm_minsize(720,640)

    def quadro_inf(self):
        self.quadro_lista = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_lista.place(relx=0.03, rely=0.48, relwidth=0.94, relheight=0.49)

        #----------------WIDGETS--------------
        #-- TREEVIEW -------------------------
        self.lista_inf = ttk.Treeview(self.quadro_lista, height=3, columns=self.NOME_COLUNA)
        self.lista_inf.place(relx=0.0, rely=0.0, relwidth=0.97, relheight=0.97)

            # Adiciona as colunas com os nomes fornecidos
        self.lista_inf.heading("#0",text="")
        for idx, nome_coluna in enumerate(self.NOME_COLUNA):
            self.lista_inf.heading(f"#{idx+1}", text=nome_coluna)

            # Configuração das colunas
        width_column = int(500/len(self.NOME_COLUNA))
        self.lista_inf.column("#0",width=0, stretch=False)
        for idx in range(len(self.NOME_COLUNA)):
            self.lista_inf.column(f"#{idx+1}", width=width_column, anchor='center', stretch=True)

        self.bar_rol = Scrollbar(self.quadro_lista, orient='vertical')
        self.lista_inf.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.97, rely=0.0, relwidth=0.03, relheight=0.97)
        self.lista_inf.bind("<Button-1>", self.atualizar_labels_entrys)

    def quadro_login(self):
        self.quadro_log = Frame(self.root, bd=4, background='lightgray', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_log.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.43)
        self.quadro_log.bind("<Configure>", self.atualizar_wraplength)

        ####################################### BOTÕES ###################################################

        self.bt_buscar = Button(self.quadro_log, text='Buscar', width=7)
        self.bt_buscar.place(relx=0.03, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_login = Button(self.quadro_log, text='entrar', command=self.login_usuario, width=7)
        self.bt_login.place(relx=0.53, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_registrar = Button(self.quadro_log, text='registre-se', width=7)
        self.bt_registrar.place(relx=0.67, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_desconto = Checkbutton(self.quadro_log)
        self.bt_desconto.place(relx=0.75, rely=0.65, relwidth=0.04, relheight=0.12)

        ####################################### ENTRYS ###################################################

        self.id_entry = Entry(self.quadro_log, validate='key', validatecommand=(self.validar_digitos, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.id_entry.place(relx=0.03, rely=0.055, relwidth=0.05, relheight=0.15)

        self.nome_entry = Entry(self.quadro_log, validate='key', validatecommand=(self.validar_string, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.nome_entry.place(relx=0.09, rely=0.055, relwidth=0.28, relheight=0.15)

        self.preco_entry = Entry(self.quadro_log, validate='key', validatecommand=(self.validar_ponto_dec, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.preco_entry.place(relx=0.22, rely=0.26, relwidth=0.09, relheight=0.15)

        self.categoria_entry = Entry(self.quadro_log, validate='key', validatecommand=(self.validar_string, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.categoria_entry.place(relx=0.03, rely=0.26, relwidth=0.18, relheight=0.15)

        self.id_user_entry = Entry(self.quadro_log, validate='key', validatecommand=(self.validar_digitos, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.id_user_entry.place(relx=0.51, rely=0.055, relwidth=0.28, relheight=0.15)
        self.id_user_entry.insert(0,"24042912431312")

        self.nome_user_entry = Entry(self.quadro_log, validate='key', validatecommand=(self.validar_string, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.nome_user_entry.place(relx=0.51, rely=0.255, relwidth=0.28, relheight=0.15)
        self.nome_user_entry.insert(0,"João Oliveira")

        self.telefone_entry = Entry(self.quadro_log, validate='key', validatecommand=(self.validar_digitos, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.telefone_entry.place(relx=0.51, rely=0.465, relwidth=0.28, relheight=0.15)

        ####################################### LABELS ###################################################

        self.id_label = Label(self.quadro_log,text="id", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.id_label.place(relx=0.03, rely=0, relwidth=0.02, relheight=0.05)

        self.nome_label = Label(self.quadro_log,text="nome", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.nome_label.place(relx=0.09, rely=0, relwidth=0.05, relheight=0.05)

        self.preco_label = Label(self.quadro_log,text="preço", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.preco_label.place(relx=0.22, rely=0.205, relwidth=0.04, relheight=0.05)

        self.categoria_label = Label(self.quadro_log,text="categoria", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.categoria_label.place(relx=0.03, rely=0.205, relwidth=0.07, relheight=0.05)

        self.descricao_label = Label(self.quadro_log,text="", justify='left',font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.descricao_label.place(relx=0.03, rely=0.42, relwidth=0.34, relheight=0.42)

        self.id_user_label = Label(self.quadro_log,text="id", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.id_user_label.place(relx=0.51, rely=0, relwidth=0.02, relheight=0.05)

        self.nome_user_label = Label(self.quadro_log,text="nome do usuário", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.nome_user_label.place(relx=0.51, rely=0.205, relwidth=0.1, relheight=0.05)
        
        self.telefone_label = Label(self.quadro_log,text="telefone", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.telefone_label.place(relx=0.51, rely=0.41, relwidth=0.05, relheight=0.05)

        self.desconto_label = Label(self.quadro_log, text="Flamengo/One Piece/Souza ?", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.desconto_label.place(relx=0.51,rely=0.65, relwidth=0.18, relheight=0.08)

    def quadro_cliente(self):
        self.quadro_cli = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_cli.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.43)

        ####################################### ABAS #####################################################

        self.aba = ttk.Notebook(self.quadro_cli)
        self.aba.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.aba_compra = Frame(self.aba)
        self.aba_compra.configure(background='lightgray')
        self.aba_compra.bind("<Configure>", self.atualizar_wraplength)
        self.aba.add(self.aba_compra, text= "Pedir")

        self.aba_perfil = Frame(self.aba)
        self.aba_perfil.configure(background= 'lightgray')
        self.aba.add(self.aba_perfil, text= "Perfil")

        self.aba_pedidos = Frame(self.aba)
        self.aba_pedidos.configure(background= 'lightgray')
        self.aba.add(self.aba_pedidos, text= "Pedidos")

        ####################################### BOTÕES ###################################################

        self.bt_adicionar = Button(self.aba_compra, text='Adicionar', width=7)
        self.bt_adicionar.place(relx=0.03, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_remover = Button(self.aba_compra, text='Remover', width=7)
        self.bt_remover.place(relx=0.15, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_buscar = Button(self.aba_compra, text='Buscar', width=7)
        self.bt_buscar.place(relx=0.27, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_pedir = Button(self.aba_compra, text='Pedir', width=7)
        self.bt_pedir.place(relx=0.87, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        ####################################### ENTRYS ###################################################

        self.id_entry = Entry(self.aba_compra, validate='key', validatecommand=(self.validar_digitos, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.id_entry.place(relx=0.03, rely=0.055, relwidth=0.05, relheight=0.15)

        self.nome_entry = Entry(self.aba_compra, validate='key', validatecommand=(self.validar_string, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.nome_entry.place(relx=0.09, rely=0.055, relwidth=0.28, relheight=0.15)

        self.preco_entry = Entry(self.aba_compra, validate='key', validatecommand=(self.validar_ponto_dec, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.preco_entry.place(relx=0.22, rely=0.26, relwidth=0.09, relheight=0.15)

        self.categoria_entry = Entry(self.aba_compra, validate='key', validatecommand=(self.validar_string, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.categoria_entry.place(relx=0.03, rely=0.26, relwidth=0.18, relheight=0.15)
        
        self.qtd_entry = Entry(self.aba_compra, validate='key', validatecommand=(self.validar_digitos, '%P'), justify='left', font=("Arial", 12), bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.qtd_entry.place(relx=0.32, rely=0.26, relwidth=0.05, relheight=0.15)

        ####################################### LABELS ###################################################

        self.id_label = Label(self.aba_compra,text="id", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.id_label.place(relx=0.03, rely=0, relwidth=0.02, relheight=0.05)

        self.nome_label = Label(self.aba_compra,text="nome", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.nome_label.place(relx=0.09, rely=0, relwidth=0.05, relheight=0.05)

        self.qtd_label = Label(self.aba_compra,text="qtd", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.qtd_label.place(relx=0.32, rely=0.205, relwidth=0.04, relheight=0.05)

        self.preco_label = Label(self.aba_compra,text="preço", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.preco_label.place(relx=0.22, rely=0.205, relwidth=0.04, relheight=0.05)

        self.categoria_label = Label(self.aba_compra,text="categoria", justify='left', font=('Arial',10),bg='lightgray', fg="#403d3d")
        self.categoria_label.place(relx=0.03, rely=0.205, relwidth=0.07, relheight=0.05)

        self.descricao_label = Label(self.aba_compra,text="", justify='left',font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.descricao_label.place(relx=0.03, rely=0.42, relwidth=0.34, relheight=0.42)

        self.id_perfil_label = Label(self.aba_perfil, text="id", justify='left',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.id_perfil_label.place(relx=0.325, rely=0.08, relwidth=0.35, relheight=0.15)

        self.nome_perfil_label = Label(self.aba_perfil,text="nome", justify='left',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.nome_perfil_label.place(relx=0.325, rely=0.29, relwidth=0.35, relheight=0.15)

        self.telefone_perfil_label = Label(self.aba_perfil, text="telefone", justify='left',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.telefone_perfil_label.place(relx=0.325, rely=0.495, relwidth=0.35, relheight=0.15)

        self.desconto_perfil_label = Label(self.aba_perfil, text="Flamengo/One Piece/Souza", justify='left',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.desconto_perfil_label.place(relx=0.325, rely=0.70, relwidth=0.35, relheight=0.15)

        ####################################### TREEVIEW CARRINHO ########################################

        carrinho = ["nome","preço","qtd","total"]
        self.lista_carrinho = ttk.Treeview(self.aba_compra, height=3, columns=carrinho)
        self.lista_carrinho.place(relx=0.4, rely=0.0, relwidth=0.57, relheight=0.84)

            # Adiciona as colunas com os nomes fornecidos
        self.lista_carrinho.heading("#0",text="")
        for idx, nome_coluna in enumerate(carrinho):
            self.lista_carrinho.heading(f"#{idx+1}", text=nome_coluna)

            # Configuração das colunas
        width_column = int(500/len(carrinho))
        self.lista_carrinho.column("#0",width=0, stretch=False)
        for idx in range(len(carrinho)):
            self.lista_carrinho.column(f"#{idx+1}", width=width_column, stretch=True)
        
        self.bar_rol_car = Scrollbar(self.aba_compra, orient='vertical')
        self.lista_carrinho.configure(yscroll=self.bar_rol_car.set)
        self.bar_rol_car.place(relx=0.97, rely=0.0, relwidth=0.03, relheight=0.84)
        
        ####################################### TREEVIEW HISTORICO #######################################

        carrinho = ["nome","preço","qtd","total"]
        self.lista_hist = ttk.Treeview(self.aba_pedidos, height=3, columns=carrinho)
        self.lista_hist.place(relx=0, rely=0, relwidth=0.97, relheight=1)

            # Adiciona as colunas com os nomes fornecidos
        self.lista_hist.heading("#0",text="")
        for idx, nome_coluna in enumerate(carrinho):
            self.lista_hist.heading(f"#{idx+1}", text=nome_coluna)

            # Configuração das colunas
        width_column = int(500/len(carrinho))
        self.lista_hist.column("#0",width=0, stretch=False)
        for idx in range(len(carrinho)):
            self.lista_hist.column(f"#{idx+1}", width=width_column, stretch=True)
        
        self.bar_rol_hist = Scrollbar(self.aba_pedidos, orient='vertical')
        self.lista_hist.configure(yscroll=self.bar_rol_hist.set)
        self.bar_rol_hist.place(relx=0.97, rely=0.0, relwidth=0.03, relheight=1)
    
    # ------ FUNÇÕES AUXILIARES DO FRONT -------

    def atualizar_wraplength(self, event):
        if self.user_data == []:
            self.descricao_label.config(wraplength=self.quadro_log.winfo_width()*0.32)
        else:
            self.descricao_label.config(wraplength=self.aba_compra.winfo_width()*0.32)
    
    def atualizar_labels_entrys(self, event):
        selecao = self.lista_inf.focus()
        if selecao:
            if self.user_data != []:
                self.qtd_entry.delete(0,END)
                self.qtd_entry.insert(0,"1")
            
            self.categoria_entry.delete(0,END)
            self.id_entry.delete(0,END)
            self.nome_entry.delete(0,END)
            self.preco_entry.delete(0,END)

            valores = self.lista_inf.item(selecao, 'values')
            self.id_entry.insert(0,valores[0])
            self.nome_entry.insert(0,valores[1])
            self.categoria_entry.insert(0,valores[2])
            self.preco_entry.insert(0,valores[4])
            self.descricao_label.config(text=valores[3])

    #--FALTA LOGIN DE FUNCIONARIO
    def login_usuario(self):
            self.user_data = [self.id_user_entry.get(), self.nome_user_entry.get()]  
            self.user_data, user_tipo = self.get_user()

            if user_tipo == 'cliente':
                self.quadro_log.destroy()
                self.quadro_cliente()
            
            elif user_tipo == 'funcionário':
                #chamar menu de adm
                dados = "temporário"

            else: 
                messagebox.showerror("Dados errados", "Nome de usuário ou id errados, tente novamente.")
                
    def atualiza_tabela(self):
        for data in self.lista_inf.get_children():
            self.lista_inf.delete(data)

        for array in self.fsql.get_data():
            self.lista_inf.insert("", END,iid=array, text="", values=(array))

    # ------ FUNÇÕES SQL ----------------
    
    def get_user(self):
        self.fsql.conexao()
        self.fsql.cursor.execute(f"SELECT * FROM clientes WHERE id_cliente = '{self.user_data[0]}' AND nome = '{self.user_data[1]}'")
        data = self.fsql.cursor.fetchall()
        self.fsql.conn.commit()
        tipo = "cliente"

        if len(data) == 0:  # É um funcionário
            self.fsql.cursor.execute(f"SELECT * FROM funcionários WHERE id_funcionário = '{self.user_data[0]}' AND nome = '{self.user_data[1]}'")
            data = self.fsql.cursor.fetchall()
            self.fsql.conn.commit()
            tipo = "funcionário"

        if len(data) == 0:
            tipo = None

        self.fsql.conn.close()
        
        return data,tipo