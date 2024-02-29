from tkinter import *
import tkinter as tk

class Application():

    def __init__(self):
        self.root = Tk()
        self.tela()
        self.quadros()
        self.botoes()
        self.root.mainloop()

    def tela(self):
        self.root.geometry("1080x720")
        self.root.title("Gerenciador de Restaurante")
        self.root.configure(background='#005089')
        self.root.resizable(True, True)
        self.root.wm_maxsize(1188,792)
        self.root.wm_minsize(640,480)

    def quadros(self):
        self.quadro_1 = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_1.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.4)

        self.quadro_2 = Frame(self.root, bd=4, background='white', highlightbackground='#4169e1', highlightthickness=3)
        self.quadro_2.place(relx=0.03, rely=0.48, relwidth=0.94, relheight=0.49)

    def botoes(self):
        self.bt_limpar = Button(self.quadro_1, text='Limpar')
        self.bt_limpar.place(relx=0.1, rely=0.02, relwidth=0.07, relheight=0.09)
        
        self.bt_selecionar = Button(self.quadro_1, text='Selecionar')
        self.bt_selecionar.place(relx=0.1, rely=0.02, relwidth=0.07, relheight=0.09)
        
        self.bt_buscar = Button(self.quadro_1, text='Buscar')
        self.bt_buscar.place(relx=0.1, rely=0.02, relwidth=0.07, relheight=0.09)

        self.bt_adicionar = Button(self.quadro_1, text='Adicionar')
        self.bt_adicionar.place(relx=0.1, rely=0.02, relwidth=0.07, relheight=0.09)

        self.bt_editar = Button(self.quadro_1, text='Editar')
        self.bt_editar.place(relx=0.1, rely=0.02, relwidth=0.07, relheight=0.09)

        self.bt_deletar = Button(self.quadro_1, text='Deletar')
        self.bt_deletar.place(relx=0.1, rely=0.02, relwidth=0.07, relheight=0.09)

Application()