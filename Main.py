import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from Tabela_funcionario import *
from Login_bd import *
from Navegacao import *
from Tabela_pedidos import *
from Tabela_prato_pedido import *
from Tabela_cardapio import *
from Tabela_cliente import *

usuario = Login_bd()

if usuario.connection_data:
    Navegacao(usuario.connection_data, usuario.table_metadata, usuario.view_metadata)


