import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from Tabela import *
from Login_bd import *
from Navegacao import *

usuario = Login_bd()
#nomestabela = list(usuario.schema_metadata.keys())
if usuario.connection_data != []:
    Navegacao(usuario.connection_data, usuario.table_metadata, usuario.view_metadata)
#Navegacao(usuario.connection_data, "cardápio", usuario.schema_metadata["cardápio"])
#Tabela(usuario.connection_data, "cardápio", usuario.table_metadata["cardápio"])



#Tabela(usuario.connection_data, nomestabela[0], usuario.schema_metadata[nomestabela[0]])


