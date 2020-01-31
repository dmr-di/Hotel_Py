import sqlite3

import variables, conexion

def cargar_precios():
    try:
        conexion.cur.execute('SELECT * FROM precios')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar_precios():
    try:
        precios = cargar_precios()
        variables.precios[0].set_text(str(precios[0]))
        variables.precios[1].set_text(str(precios[1]))
        variables.precios[2].set_text(str(precios[2]))
    except:
        print("No hay precios guardados")

def guardar_precio(precios):
    try:
        #TODO
        pass
    except:
        print("Error actualizando precio")