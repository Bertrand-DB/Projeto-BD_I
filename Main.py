import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from Tabela import *

NOME_TABELA = "Funcionários"
NOME_COLUNA = ["Id_Funcionários", "Nome", "Cargo", "Salário"]

ESPACAMENT_Y = 0.045
X_LABEL = 0.25
L_ENTRY = 0.5
A_LABEL = 0.05
A_ENTRY = 0.08

class Login:
    def __init__(self):
        self.root = tk.Tk()

        self.tela()
        self.labels_entrys()
        self.button()
        self.root.mainloop()

    def tela(self):
        self.root.geometry("480x360")
        self.root.title("Gerenciador de Restaurante")
        self.root.configure(background='#005089')
        self.root.resizable(False, False)

    def labels_entrys(self):
        self.user_label = Label(text="User:", font=('Arial',10),bg="#005089", fg="white")
        self.user_label.place(relx=X_LABEL, rely=ESPACAMENT_Y*2+A_LABEL*0+A_ENTRY*0, relheight=A_LABEL)
        self.user_entry = Entry(width=25, justify='left', font=("Arial", 12), highlightthickness=2, highlightcolor="#006ebc", relief="ridge")
        self.user_entry.place(relx=X_LABEL, rely=ESPACAMENT_Y*2+A_LABEL*1+A_ENTRY*0, relwidth=L_ENTRY, relheight=A_ENTRY)

        self.password_label = Label(text="Password:", font=('Arial',10),bg="#005089", fg="white")
        self.password_label.place(relx=X_LABEL, rely=ESPACAMENT_Y*3+A_LABEL*1+A_ENTRY*1, relheight=A_LABEL)
        self.password_entry = Entry(width=25, justify='left', show="*", highlightthickness=2, highlightcolor="#006ebc", relief="ridge")
        self.password_entry.place(relx=X_LABEL, rely=ESPACAMENT_Y*3+A_LABEL*2+A_ENTRY*1, relwidth=L_ENTRY, relheight=A_ENTRY)

        self.host_label = Label(text="Host:", font=('Arial',10),bg="#005089", fg="white")
        self.host_label.place(relx=X_LABEL, rely=ESPACAMENT_Y*4+A_LABEL*2+A_ENTRY*2, relheight=A_LABEL)
        self.host_entry = Entry(width=25, justify='left', font=("Arial", 12), highlightthickness=2, highlightcolor="#006ebc", relief="ridge")
        self.host_entry.place(relx=X_LABEL, rely=ESPACAMENT_Y*4+A_LABEL*3+A_ENTRY*2, relwidth=L_ENTRY, relheight=A_ENTRY)

        self.database_label = Label(text="Database:", font=('Arial',10),bg="#005089", fg="white")
        self.database_label.place(relx=X_LABEL, rely=ESPACAMENT_Y*5+A_LABEL*3+A_ENTRY*3, relheight=A_LABEL)
        self.database_entry = Entry(width=25, justify='left', font=("Arial", 12), highlightthickness=2, highlightcolor="#006ebc", relief="ridge")
        self.database_entry.place(relx=X_LABEL, rely=ESPACAMENT_Y*5+A_LABEL*4+A_ENTRY*3, relwidth=L_ENTRY, relheight=A_ENTRY)

        #iniciador de login Bertrand
        self.user_entry.insert(END,"root")
        self.password_entry.insert(END,"369MyRoot*")
        self.host_entry.insert(END,"localhost")
        self.database_entry.insert(END,"Projeto-BD_I")

        '''
        #iniciador de login Rodrigo
        self.user_entry.insert(END,"root")
        self.password_entry.insert(END,"746832fC")
        self.host_entry.insert(END,"localhost")
        self.database_entry.insert(END,"teste")
        '''

    def button(self):
        self.login_bt = Button(text="LOGIN", font=("Arial",12), relief="raised", bd=2, activebackground="#006ebc", activeforeground="white", command=self.funcao_login_bt)
        self.login_bt.place(relx=0.375, rely=ESPACAMENT_Y*5+A_LABEL*4+A_ENTRY*5, relwidth=0.25, relheight=A_ENTRY)

    def valida_dados(self):
        try:
            mysql.connector.connect(
            host = self.host_entry.get(),
            user = self.user_entry.get(),
            password= self.password_entry.get(),
            database= self.database_entry.get()
        )
        except Exception:
            messagebox.showerror("ERRO!", "Não foi possível se conectar.\nVerifique seus dados, e tente novamente.")
            return False
        return True
    
    def get_dados(self):
        return [self.host_entry.get(), self.user_entry.get(), self.password_entry.get(), self.database_entry.get()]
    
    def funcao_login_bt(self):
        if not self.valida_dados():
            return
        
        CONEX_DADOS = self.get_dados()
        self.root.destroy()
        gerenciador = Tabela(CONEX_DADOS, NOME_TABELA, NOME_COLUNA)

Login()