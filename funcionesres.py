import sqlite3

import variables, conexion

def limpiarLabel():
    variables.lbldnires.set_text('')
    variables.lblapelres.set_text('')

def listarreshab():
    try:
        conexion.cur.execute('SELECT numero FROM habitaciones')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadoreshab(listreshab):
    try:
        variables.listadoreshab = listarreshab()
        listreshab.clear()
        for registro in variables.listadoreshab:
            listreshab.append(registro)
    except:
        print('Error en cargar ComboBox')