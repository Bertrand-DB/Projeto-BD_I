from tkinter import *
from tkinter import ttk
import tkinter as tk
from Validadores import *
from Funcoes_sql import *
from Tabela_cardapio import*
from Tabela_cliente import*
from Tabela_funcionario import*
from Tabela_pedidos import*
from Tabela_prato_pedido import*
import decimal

#constantes de posição dos botões
LARGURA_BT = 0.10
ALTURA_BT = 0.14
ESPACAMENTO_BT = 0.02
X_BOTAO = 1 - LARGURA_BT - ESPACAMENTO_BT

#constantes de posição das labels e entrys



class Navegacao():
    def __init__(self,CONEX_DADOS, table_metadata, view_metadata):

        self.CONEX_DADOS = CONEX_DADOS
        self.table_metadata = table_metadata
        self.view_metadata = view_metadata

        self.user_data = []
        self.carrinho = []
        self.total_carrinho = decimal.Decimal('00.00')

        self.root = tk.Tk()
        self.sql_card = Funcoes_sql(self.CONEX_DADOS,"cardápio",self.table_metadata["cardápio"])
        self.sql_cli = Funcoes_sql(self.CONEX_DADOS,"clientes",self.table_metadata["clientes"])
        self.sql_ped = Funcoes_sql(self.CONEX_DADOS, "pedidos_cliente",self.view_metadata["pedidos_cliente"])
        self.sql_func = Funcoes_sql(self.CONEX_DADOS,"funcionários",self.table_metadata["funcionários"])
        self.sql_pedir = Funcoes_sql(self.CONEX_DADOS, "pedidos",self.table_metadata["pedidos"])
        self.sql_pra_ped = Funcoes_sql(self.CONEX_DADOS, "pratos_pedidos",self.table_metadata["pratos_pedidos"])
        self.valida = Validadores()

        self.validar_digitos = self.root.register(self.valida.digitos)         #permite o tkinter reconhecer os validadores
        self.validar_ponto_dec = self.root.register(self.valida.ponto_decimal)
        self.validar_string = self.root.register(self.valida.string)

        self.tela()
        self.quadro_inf()
        self.quadro_login()
        self.atualiza_cardapio()
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

        #-- TREEVIEW -------------------------
        cardapio = ["id_prato", "nome", "categoria", "descrição", "preço"]
        self.lista_inf = ttk.Treeview(self.quadro_lista, height=3, columns=cardapio)
        self.lista_inf.place(relx=0.0, rely=0.0, relwidth=0.97, relheight=0.97)

            # Adiciona as colunas com os nomes fornecidos
        self.lista_inf.heading("#0",text="")
        for idx, nome_coluna in enumerate(cardapio):
            self.lista_inf.heading(f"#{idx+1}", text=nome_coluna)

            # Configuração das colunas
        width_column = int(500/len(cardapio))
        self.lista_inf.column("#0",width=0, stretch=False)
        for idx in range(len(cardapio)):
            self.lista_inf.column(f"#{idx+1}", width=width_column, anchor='center', stretch=True)

        self.bar_rol = Scrollbar(self.quadro_lista, orient='vertical')
        self.lista_inf.configure(yscroll=self.bar_rol.set)
        self.bar_rol.place(relx=0.97, rely=0.0, relwidth=0.03, relheight=0.97)
        self.lista_inf.bind("<Double-1>", self.atualizar_labels_entrys)

    def quadro_login(self):
        self.quadro_log = Frame(self.root, bd=4, background='lightgray', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_log.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.43)
        self.quadro_log.bind("<Configure>", self.atualizar_wraplength)

        ####################################### BOTÕES ###################################################

        self.bt_buscar = Button(self.quadro_log, text='Buscar', command=self.mostrar_busca, width=7)
        self.bt_buscar.place(relx=0.03, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_login = Button(self.quadro_log, text='entrar', command=self.login_usuario, width=7)
        self.bt_login.place(relx=0.53, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_registrar = Button(self.quadro_log, text='registre-se', command=self.registra_usuario, width=7)
        self.bt_registrar.place(relx=0.67, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.estado_checkbox = BooleanVar()
        self.bt_desconto = Checkbutton(self.quadro_log, variable=self.estado_checkbox)
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
        self.id_user_entry.insert(0,"24043013165960")
        #self.id_user_entry.insert(0,"24043013165997")

        self.nome_user_entry = Entry(self.quadro_log, validate='key', validatecommand=(self.validar_string, '%P'), font=('Arial',12),bg="#feffff", fg="#403d3d", highlightthickness=2)
        self.nome_user_entry.place(relx=0.51, rely=0.255, relwidth=0.28, relheight=0.15)
        self.nome_user_entry.insert(0,"Maria Santos")
        #self.nome_user_entry.insert(0,"Maria Oliveira")

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

        self.bt_adicionar = Button(self.aba_compra, text='Adicionar', command=self.adiciona_carrinho, width=7)
        self.bt_adicionar.place(relx=0.03, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_remover = Button(self.aba_compra, text='Remover', command=self.remove_carrinho, width=7)
        self.bt_remover.place(relx=0.15, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_buscar = Button(self.aba_compra, text='Buscar', command=self.mostrar_busca, width=7)
        self.bt_buscar.place(relx=0.27, rely=0.85, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_pedir = Button(self.aba_compra, text='Pedir', command=self.pedir, width=7)
        self.bt_pedir.place(relx=0.87, rely=0.85, relwidth=0.12, relheight=ALTURA_BT)

        self.pagamento = StringVar(value="Cartão")
        self.bt_pagamento1 = Radiobutton(self.aba_compra, text="Cartão", variable=self.pagamento, value="Cartão")
        self.bt_pagamento1.place(relx=0.42, rely=0.88)

        self.bt_pagamento2 = Radiobutton(self.aba_compra, text="Boleto", variable=self.pagamento, value="Boleto")
        self.bt_pagamento2.place(relx=0.50, rely=0.88)

        self.bt_pagamento3 = Radiobutton(self.aba_compra, text="Pix", variable=self.pagamento, value="Pix")
        self.bt_pagamento3.place(relx=0.58, rely=0.88)

        self.bt_pagamento4 = Radiobutton(self.aba_compra, text="Berries", variable=self.pagamento, value="Berries")
        self.bt_pagamento4.place(relx=0.64, rely=0.88)

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

        self.id_perfil_label = Label(self.aba_perfil, text="Id: "+self.user_data[0], justify='left',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.id_perfil_label.place(relx=0.325, rely=0.08, relwidth=0.35, relheight=0.15)

        self.nome_perfil_label = Label(self.aba_perfil,text="Nome: "+self.user_data[1], justify='left',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.nome_perfil_label.place(relx=0.325, rely=0.29, relwidth=0.35, relheight=0.15)

        self.telefone_perfil_label = Label(self.aba_perfil, text="Telefone: "+self.user_data[2], justify='left',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.telefone_perfil_label.place(relx=0.325, rely=0.495, relwidth=0.35, relheight=0.15)

        if self.user_data[3]: desconto_txt = "Sim"
        else: desconto_txt = "Não"

        self.desconto_perfil_label = Label(self.aba_perfil, text="Flamengo/One Piece/Souza? "+desconto_txt, justify='left',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.desconto_perfil_label.place(relx=0.325, rely=0.70, relwidth=0.35, relheight=0.15)

        self.total_label = Label(self.aba_compra, text="R$ 00.00", justify='center',font=('Arial',12),bg="white", fg="#403d3d",relief='ridge', highlightthickness=2)
        self.total_label.place(relx=0.73, rely=0.85, relwidth=0.12, relheight=ALTURA_BT)

        ####################################### TREEVIEW CARRINHO ########################################

        carrinho = ["id","nome","preço","qtd","sub_total"]
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
            self.lista_carrinho.column(f"#{idx+1}", width=width_column, anchor='center', stretch=True)
        
        self.bar_rol_car = Scrollbar(self.aba_compra, orient='vertical')
        self.lista_carrinho.configure(yscroll=self.bar_rol_car.set)
        self.bar_rol_car.place(relx=0.97, rely=0.0, relwidth=0.03, relheight=0.84)
        
        ####################################### TREEVIEW PEDIDOS #########################################

        self.lista_hist = ttk.Treeview(self.aba_pedidos, height=3, columns=self.view_metadata["pedidos_cliente"])
        self.lista_hist.place(relx=0, rely=0, relwidth=0.97, relheight=1)

            # Adiciona as colunas com os nomes fornecidos
        self.lista_hist.heading("#0",text="")
        for idx, nome_coluna in enumerate(self.view_metadata["pedidos_cliente"]):
            self.lista_hist.heading(f"#{idx+1}", text=nome_coluna)

            # Configuração das colunas
        width_column = int(500/len(self.view_metadata["pedidos_cliente"]))
        self.lista_hist.column("#0",width=0, stretch=False)
        for idx in range(len(self.view_metadata["pedidos_cliente"])):
            self.lista_hist.column(f"#{idx+1}", width=width_column, anchor='center', stretch=True)
        
        self.bar_rol_hist = Scrollbar(self.aba_pedidos, orient='vertical')
        self.lista_hist.configure(yscroll=self.bar_rol_hist.set)
        self.bar_rol_hist.place(relx=0.97, rely=0.0, relwidth=0.03, relheight=1)
    
    def quadro_funcionario(self):
        self.root.geometry("720x640")


        ##################### LABELS #####################
        estilo_entry = {
            'font': ('Arial', 12),
            'bg': 'white',
            'fg': '#403d3d',
            'readonlybackground': 'white',
            'selectbackground': '#3272a0',
            'selectforeground': 'white',
            'borderwidth': 0,
            'highlightthickness': 2,
            'highlightbackground': '#3272a0',
            'relief': 'ridge',
            'justify': 'center'
            }
        self.id_label = Entry(self.root, **estilo_entry)
        self.id_label.insert(0, self.user_data[0])
        self.id_label.configure(state='readonly')
        self.id_label.place(relx=0.20, rely=0.03, relwidth=0.25, relheight=0.05)

        self.nome_label = Label(self.root, text=self.user_data[1], justify='left', font=('Arial',12),bg='white', fg="#403d3d", relief='ridge', highlightthickness=2, highlightbackground='#3272a0')
        self.nome_label.place(relx=0.58, rely=0.03, relwidth=0.25, relheight=0.05)

        ##################### BOTÕES #####################
        
        self.clientes_bt = Button(width=25, text='Clientes', command=self.bt_clientes, font=("Arial",12), relief="raised", bd=3, activebackground="#006ebc", activeforeground="white")
        self.clientes_bt.place(relx=0.25, rely=0.17, relwidth=0.5, relheight=0.08)

        self.funcionarios_bt = Button(width=25, text='Funcionários', command=self.bt_funcionarios, font=("Arial",12), relief="raised", bd=3, activebackground="#006ebc", activeforeground="white")
        self.funcionarios_bt.place(relx=0.25, rely=0.33, relwidth=0.5, relheight=0.08)

        self.cardapio_bt = Button(width=25, text='Cardápio', command=self.bt_cardapio, font=("Arial",12), relief="raised", bd=3, activebackground="#006ebc", activeforeground="white")
        self.cardapio_bt.place(relx=0.25, rely=0.49, relwidth=0.5, relheight=0.08)

        self.pedidos_bt = Button(width=25, text='Pedidos', command=self.bt_pedidos, font=("Arial",12), relief="raised", bd=3, activebackground="#006ebc", activeforeground="white")
        self.pedidos_bt.place(relx=0.25, rely=0.65, relwidth=0.5, relheight=0.08)

        self.pratos_ped_bt = Button(width=25, text='Pratos Pedidos', command=self.bt_pratos_ped, font=("Arial",12), relief="raised", bd=3, activebackground="#006ebc", activeforeground="white")
        self.pratos_ped_bt.place(relx=0.25, rely=0.81, relwidth=0.5, relheight=0.08)

    # ------ FUNÇÕES AUXILIARES DO FRONT -------

    def atualizar_wraplength(self, event):
        if self.user_data == []:
            self.descricao_label.config(wraplength=self.quadro_log.winfo_width()*0.32)
        else:
            self.descricao_label.config(wraplength=self.aba_compra.winfo_width()*0.32)
    
    def atualizar_labels_entrys(self, event):
        selecao = self.lista_inf.selection()[0]
        if selecao:
            if self.user_data:
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

    def limpa_entrys(self):
        if self.user_data:
           self.qtd_entry.delete(0,END) 

        self.id_entry.delete(0,END)
        self.nome_entry.delete(0,END)
        self.categoria_entry.delete(0,END)
        self.preco_entry.delete(0,END)
        self.descricao_label.config(text="")

    def login_usuario(self):
            self.user_data = [self.id_user_entry.get(), self.nome_user_entry.get()]  
            self.user_data, user_tipo = self.get_user()

            if user_tipo == 'cliente':
                self.quadro_log.destroy()
                self.quadro_cliente()
                self.atualiza_pedidos()
            
            elif user_tipo == 'funcionário':
                self.quadro_log.destroy()
                self.quadro_lista.destroy()
                self.quadro_funcionario()

            else: 
                messagebox.showerror("Dados errados", "Nome de usuário ou id errados, tente novamente.")
                
    def atualiza_cardapio(self):
        for data in self.lista_inf.get_children():
            self.lista_inf.delete(data)

        for array in self.get_cardapio():
            self.lista_inf.insert("", END,iid=array, text="", values=(array))

    def atualiza_pedidos(self):
        for data in self.lista_hist.get_children():
            self.lista_hist.delete(data)

        for array in self.get_pedidos_cliente():
            self.lista_hist.insert("", END,iid=array, text="", values=(array))

    def atualiza_carrinho(self):
        for data in self.lista_carrinho.get_children():
            self.lista_carrinho.delete(data)

        for array in self.carrinho:
            self.lista_carrinho.insert("", END,iid=array, text="", values=(array))

    def atualiza_total(self):
        total = decimal.Decimal('00.00')
        for item in self.carrinho:
            total += item[4]
        
        self.total_carrinho = total
        self.total_label.config(text="R$ "+str(self.total_carrinho))

    def adiciona_carrinho(self):
        self.sql_card.conexao()
        self.sql_card.cursor.execute(f"SELECT id_prato, nome, preço FROM cardápio WHERE id_prato = '{self.id_entry.get()}'")
        pedido = self.sql_card.cursor.fetchall()[0]
        self.sql_card.conn.commit()
        self.sql_card.conn.close()

        id = pedido[0]
        nome = pedido[1]
        preco = pedido[2]
        qtd = int(self.qtd_entry.get())

        if len(pedido) == 0:
            messagebox.showerror("Prato não encontrado", "Não foi possível encontrar o prato, verifique o id do prato escolhido e tente novamente.")
            return

        ja_tem = False
        # procura o pedido no carrinho, e acrescenta se já tiver
        for item in self.carrinho:
            if id == item[0]:
                item[3] += qtd
                item[4] = item[2]*item[3]*(1 - decimal.Decimal('00.15')*self.user_data[3])
                item[4] = decimal.Decimal(item[4]).quantize(decimal.Decimal('0.01'))
                ja_tem = True
                break
        
        if not ja_tem:
            total = preco*qtd * (1 - decimal.Decimal('00.15')*self.user_data[3])   #aplica desconto se existir
            total = decimal.Decimal(total).quantize(decimal.Decimal('0.01'))
            self.carrinho.append([id, nome, preco, qtd, total])

        self.limpa_entrys()
        self.atualiza_total()
        self.atualiza_carrinho()

    def remove_carrinho(self):
        id = int(self.id_entry.get())
        qtd = int(self.qtd_entry.get())

        remover = None
        tem = False
        for i, item in enumerate(self.carrinho):
            if item[0] == id:
                item[3] -= qtd
                item[4] = item[2]*item[3]*(1 - decimal.Decimal('00.15')*self.user_data[3])
                item[4] = decimal.Decimal(item[4]).quantize(decimal.Decimal('0.01'))
                tem = True
                if item[3] <= 0:
                    remover = i
                break

        if not tem:
            messagebox.showerror("Prato não encontrado", "Não foi possível encontrar o prato, verifique o id do prato escolhido e tente novamente.")
            return
        
        if remover is not None:
            del self.carrinho[remover]

        self.limpa_entrys()
        self.atualiza_total()
        self.atualiza_carrinho()
    
    def mostrar_busca(self):
        for data in self.lista_inf.get_children():
            self.lista_inf.delete(data)

        for array in self.buscar():
            self.lista_inf.insert("", END,iid=array, text="", values=(array))

        self.limpa_entrys()

    def copiar_texto(self, event):
        self.root.clipboard_clear()  # Limpa o conteúdo atual da área de transferência
        self.root.clipboard_append(string=str(self.user_data[0]))

    def bt_cardapio(self):
        card = Tabela_cardapio(self.CONEX_DADOS, "cardápio", self.table_metadata["cardápio"])
    
    def bt_clientes(self):
        cli = Tabela_cliente(self.CONEX_DADOS, "clientes", self.table_metadata["clientes"])

    def bt_funcionarios(self):
        func = Tabela_funcionario(self.CONEX_DADOS, "funcionários", self.table_metadata["funcionários"])

    def bt_pedidos(self):
        ped = Tabela_pedidos(self.CONEX_DADOS, "pedidos", self.table_metadata["pedidos"])

    def bt_pratos_ped(self):
        prat = Tabela_prato_pedido(self.CONEX_DADOS, "pratos_pedidos", self.table_metadata["pratos_pedidos"])
        
    # ------ FUNÇÕES SQL ----------------
    def registra_usuario(self):

        if self.id_entry.get() != "":
            messagebox.showinfo("Id não cadastrado", "O cadastro de id é gerado automaticamente pelo sistema.")

        self.user_data = [self.nome_user_entry.get(), self.telefone_entry.get(), self.estado_checkbox.get()] 
        
        try:
            
            self.sql_cli.conexao()
            self.sql_cli.cursor.callproc("inserir_cliente", self.user_data)
            self.sql_cli.conn.commit()

            self.sql_cli.cursor.execute(f"SELECT * FROM clientes WHERE nome = '{self.user_data[0]}'")
            data = self.sql_cli.cursor.fetchall()
            self.sql_cli.conn.commit()
            self.user_data = list(data[0])

            self.quadro_log.destroy()
            self.quadro_cliente()
            self.atualiza_pedidos()

        except Exception as e:
            messagebox.showerror("Erro ao registrar", e)

        finally:
            self.sql_cli.conn.close()
 
    def get_user(self):
        self.sql_cli.conexao()
        self.sql_cli.cursor.execute(f"SELECT * FROM clientes WHERE id_cliente = '{self.user_data[0]}' AND nome = '{self.user_data[1]}'")
        data = self.sql_cli.cursor.fetchall()
        self.sql_cli.conn.commit()
        self.sql_cli.conn.close()
        tipo = "cliente"

        if len(data) == 0:  # É um funcionário
            self.sql_func.conexao()
            self.sql_func.cursor.execute(f"SELECT * FROM funcionários WHERE id_funcionário = '{self.user_data[0]}' AND nome = '{self.user_data[1]}'")
            data = self.sql_func.cursor.fetchall()
            self.sql_func.conn.commit()
            self.sql_func.conn.close()
            tipo = "funcionário"
        
        if len(data) == 0:
            return [],None

        return list(data[0]),tipo
    
    def get_pedidos_cliente(self):
        self.sql_ped.conexao()
        self.sql_ped.cursor.execute(f"SELECT * FROM pedidos_cliente WHERE nome_cliente = '{self.user_data[1]}'")
        data = self.sql_ped.cursor.fetchall()
        self.sql_ped.conn.commit()
        self.sql_ped.conn.close()

        return data
    
    def get_cardapio(self):
        self.sql_card.conexao()
        self.sql_card.cursor.execute(f"SELECT id_prato, nome, categoria, descrição, preço FROM cardápio")
        data = self.sql_card.cursor.fetchall()
        self.sql_card.conn.commit()
        self.sql_card.conn.close()
        return data

    
    def pedir(self):
        try:
            self.sql_pedir.conexao()
            self.sql_pedir.cursor.execute(f"INSERT INTO pedidos (id_cliente, total, pagamento) VALUES ('{self.user_data[0]}', '{self.total_carrinho}', '{self.pagamento.get()}')")
            pedido_id = self.sql_pedir.cursor.lastrowid
            self.sql_pedir.conn.commit()
            

            self.sql_pra_ped.conexao()
            for item in self.carrinho:
                self.sql_pra_ped.cursor.execute(f"INSERT INTO pratos_pedidos (id_pedido, id_prato, quantidade) VALUES ('{pedido_id}', '{item[0]}', '{item[3]}')")
                self.sql_pra_ped.conn.commit()
            
        except mysql.connector.errors as e:
            messagebox.showerror("Erro ao enviar o pedido", e)

        else:
            self.carrinho = []
            self.total_carrinho = decimal.Decimal('00.00')
            self.total_label.config(text=self.carrinho)
            self.atualiza_carrinho()
            self.atualiza_pedidos()
            self.atualiza_cardapio()


        finally:
            self.sql_pedir.conn.close()
            self.sql_pra_ped.conn.close()

    def buscar(self):
        busca_cmd = "SELECT id_prato, nome, categoria, descrição, preço FROM cardápio WHERE"
        and_flag = False

        if self.id_entry.get() != "":
            busca_cmd += " id_prato = " + f"'{self.id_entry.get()}'"
            and_flag = True
        
        if self.nome_entry.get() != "":
            if and_flag:
                busca_cmd += " AND"
            busca_cmd += " nome LIKE " + f"'%{self.nome_entry.get()}%'"
            and_flag = True

        if self.categoria_entry.get() != "":
            if and_flag:
                busca_cmd += " AND"
            busca_cmd += " categoria LIKE " + f"'%{self.categoria_entry.get()}%'"
            and_flag = True

        if self.preco_entry.get() != "":
            if and_flag:
                busca_cmd += " AND"
            busca_cmd += " preço <= " + f"'{self.preco_entry.get()}'"
            and_flag = True

        if not and_flag:
            busca_cmd = "SELECT id_prato, nome, categoria, descrição, preço FROM cardápio"

        self.sql_card.conexao()
        self.sql_card.cursor.execute(busca_cmd)
        data = self.sql_card.cursor.fetchall()
        self.sql_card.conn.commit()
        self.sql_card.conn.close()
        return data
        
        