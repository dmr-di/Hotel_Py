import os
import sqlite3

class Conexion:
    def abrirbbdd(self):
        try:
            global bbdd, conex, cur
            bbdd = 'Empresa.sqlite'         #Variable que almacena la bd
            conex = sqlite3.connect(bbdd)   #La abrimos
            cur = conex.cursor()            #La variable cursor
            print('Conexión realizada correctamente')
        except sqlite3.OperationalError as e:
            print('Error al abrir: ', e)

    def cerrarbbdd(self):
        try:
            cur.close()
            conex.close()
            print('Base de datos cerrada correctamente')
        except sqlite3.OperationalError as e:
            print('Error al cerrar: ', e)