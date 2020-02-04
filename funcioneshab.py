#coding=utf-8

"""Módulo que gestiona las habitaciones.

Contiene las siguientes funciones:

"""

import sqlite3

import variables, conexion


def limpiarEntry(fila):
    """
    Limpia los widgets del apartado de habitaciones.
        :param fila: Lista que contiene los widgets.
        :return: No retorna nada.

    """
    for i in range(len(fila)):
        fila[i].set_text('')
    variables.switch.set_active(True)

def seleccionRB():
    """
    Controla la selección de los radiobutton y devuelve su valor correspondiente.
        :return: Retorna el tipo de habitación.

    """
    try:
        if (variables.rbgrouphab[0].get_active()):
            tipo = 'Simple'
        elif (variables.rbgrouphab[1].get_active()):
            tipo = 'Doble'
        else:
            tipo = 'Familiar'
        return tipo
    except:
        print('Error funcion rb')

def seleccionSwitch():
    """
    Controla la selección del switch de habitaciones.
        :return: Retorna el estado de la habitación.

    """
    try:
        if (variables.switch.get_active()):
            libre = 'Si'
        else:
            libre = 'No'
        return libre
    except:
        print("Error función switch")

def insertarhab(fila):
    """
    Realiza una inserción de una habitación en la base de datos.
        :param fila: Lista que contiene los campos de una habitación.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute("INSERT INTO habitaciones (numero, tipo, precio, libre) VALUES (?,?,?,?)", fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    """
    Lista todas las habitaciones existentes en la base de datos para cargar el treeview.
        :return: Retorna una lista con todas las habitaciones.

    """
    try:
        conexion.cur.execute('SELECT numero, tipo, precio, libre FROM habitaciones')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadohab(listhabitaciones):
    """
    Carga las habitaciones registradas en la base de datos sobre el treeview.
        :param listhabitaciones: Almacena el treeview.
        :return: No retorna nada.

    """
    try:
        variables.listadohab = listar()
        listhabitaciones.clear()
        for registro in variables.listadohab:
            listhabitaciones.append(registro)
    except:
        print('Error en cargar treeview')

def bajahab(num):
    """
    Realiza un borrado de una habitación en la base de datos.
        :param num: Almacena el número de la habitación a borrar.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('DELETE FROM habitaciones WHERE numero = ?', (num,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def modifhab(registro):
    """
    Realiza una modificación de una habitación en la base de datos.
        :param registro: Lista con los datos a modificar de la habitación.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('UPDATE habitaciones SET numero = ?, tipo = ?, precio = ?, libre = ? WHERE numero = ?', (registro[0], registro[1], registro[2], registro[3], registro[0]))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()