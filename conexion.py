#coding=utf-8
import os
import sqlite3


class Conexion:
    """Módulo que gestiona la conexión con la base de datos.

    Contiene las siguientes funciones:

    """
    def abrirbbdd(self):
        """
        Abre la base de datos.
            :return: No retorna nada.

        """
        try:
            global bbdd, conex, cur
            bbdd = 'Empresa.sqlite'         #Variable que almacena la bd
            conex = sqlite3.connect(bbdd)   #La abrimos
            cur = conex.cursor()            #La variable cursor
            print('Conexión realizada correctamente')
        except sqlite3.OperationalError as e:
            print('Error al abrir: ', e)

    def cerrarbbdd(self):
        """
        Cierra la base de datos.
            :return: No retorna nada.

        """
        try:
            cur.close()
            conex.close()
            print('Base de datos cerrada correctamente')
        except sqlite3.OperationalError as e:
            print('Error al cerrar: ', e)