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

#Navegacao(usuario.connection_data, "cardápio", usuario.schema_metadata["cardápio"])


Navegacao(usuario.connection_data, "cardápio", usuario.schema_metadata["cardápio"])
#Tabela(usuario.connection_data, nomestabela[0], usuario.schema_metadata[nomestabela[0]])


