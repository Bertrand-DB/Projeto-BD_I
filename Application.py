from tkinter import *
import tkinter as tk

LARGURA_BT = 0.1
ALTURA_BT = 0.14
ESPACAMENTO_Y = 0.02
X_BOTAO = 0.89

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
        self.bt_limpar.place(relx=X_BOTAO, rely=ESPACAMENTO_Y*1 + ALTURA_BT*0, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_selecionar = Button(self.quadro_1, text='Selecionar')
        self.bt_selecionar.place(relx=X_BOTAO, rely=ESPACAMENTO_Y*2 + ALTURA_BT*1, relwidth=LARGURA_BT, relheight=ALTURA_BT)
        
        self.bt_buscar = Button(self.quadro_1, text='Buscar')
        self.bt_buscar.place(relx=X_BOTAO, rely=ESPACAMENTO_Y*3 + ALTURA_BT*2, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_adicionar = Button(self.quadro_1, text='Adicionar')
        self.bt_adicionar.place(relx=X_BOTAO, rely=ESPACAMENTO_Y*4 + ALTURA_BT*3, relwidth=LARGURA_BT, relheight=ALTURA_BT)
 
        self.bt_editar = Button(self.quadro_1, text='Editar')
        self.bt_editar.place(relx=X_BOTAO, rely=ESPACAMENTO_Y*5 + ALTURA_BT*4, relwidth=LARGURA_BT, relheight=ALTURA_BT)

        self.bt_deletar = Button(self.quadro_1, text='Deletar')
        self.bt_deletar.place(relx=X_BOTAO, rely=ESPACAMENTO_Y*6 + ALTURA_BT*5, relwidth=LARGURA_BT, relheight=ALTURA_BT)

Application()