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
#nomestabela = list(usuario.schema_metadata.keys())

#Navegacao(usuario.connection_data, "cardápio", usuario.schema_metadata["cardápio"])


#Navegacao(usuario.connection_data, usuario.table_metadata, usuario.view_metadata)
#Tabela(usuario.connection_data, nomestabela[0], usuario.schema_metadata[nomestabela[0]])
Tabela_funcionario(usuario.connection_data, "funcionários", usuario.table_metadata["funcionários"])
