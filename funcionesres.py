#coding=utf-8

"""Módulo que gestiona las reservas.

Contiene las siguientes funciones:

"""

import sqlite3

import variables, conexion

def limpiarLabel():
    """
    Limpia los label con los datos del cliente y el numero de noches.
        :return: No retorna nada.

    """
    variables.lbldnires.set_text('')
    variables.lblapelres.set_text('')
    variables.lblnoches.set_text('')

def limpiarEntry(fila):
    """
    Limpia los entry donde se da entrada a los datos.
        :param fila: Lista que contiene los widgets a limpiar.
        :return: No retorna nada.

    """
    limpiarLabel()
    for i in range(len(fila)):
        fila[i].set_text('')
    variables.cbreshab.set_active(-1)

def listarreshab():
    """
    Carga los números de las habitaciones registradas.
        :return: Retorna una lista con los números de las habitaciones.

    """
    try:
        conexion.cur.execute('SELECT numero FROM habitaciones')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    """
    Carga los datos de las reservas registradas a una lista.
        :return: Retorna una lista con los datos de las reservas.

    """
    try:
        conexion.cur.execute('SELECT cod, dni, apel, nhab, chk_in, chk_out FROM reservas')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadoreshab(listreshab):
    """
    Escribe los numeros de las habitaciones en un ComboBox.
        :param listreshab: Almacena el widget donde cargaremos los datos.
        :return: No retorna nada.

    """
    try:
        variables.listadoreshab = listarreshab()
        listreshab.clear()
        for registro in variables.listadoreshab:
            listreshab.append(registro)
    except:
        print('Error en cargar ComboBox')

def insertarres(fila):
    """
    Realiza una inserción de una reserva en la base de datos.
        :param fila: Lista que almacena los datos de la reserva.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute("INSERT INTO reservas (dni, apel, nhab, chk_in, chk_out) VALUES (?,?,?,?,?)", fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadores(listreservas):
    """
    Escribe los datos de las reservas contenidas en la base de datos sobre el treeview.
        :param listreservas: Almacena el treeview de reservas.
        :return: No retorna nada.

    """
    try:
        variables.listadores = listar()
        listreservas.clear()
        for registro in variables.listadores:
            listreservas.append(registro)
    except:
        print('Error en cargar treeview')

def bajares(cod):
    """
    Realiza un borrado de una reserva en la base de datos.
        :param cod: Almacena el código de la reserva que se desea borrar.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('DELETE FROM reservas WHERE cod = ?', (cod,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def modifres(registro):
    """
    Realiza una modificación de una reserva en la base de datos.
        :param registro: Lista que almacena los nuevos datos de la reserva.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('UPDATE reservas SET dni = ?, apel = ?, nhab = ?, chk_in = ?, chk_out = ? WHERE cod = ?', (registro[1], registro[2], registro[3], registro[4], registro[5], registro[0]))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def selecregistro(nhab):
    """
    Carga la posición del ComboBox seleccionada para devolver el número de registro.
        :param nhab: Almacena el número de la habitación seleccionada.
        :return: Retorna el número de registro.

    """
    try:
        conexion.cur.execute("select (select count(*) from habitaciones b where a.numero >= b.numero) as cnt from habitaciones a where numero = ?", (nhab,))
        nregistro = conexion.cur.fetchone()
        conexion.conex.commit()
        return nregistro
    except:
        print("Error en el numero de registro")

def habocupada(nhab, libre):
    """
    Modifica el estado de una habitación.
        :param nhab: Almacena el número de la habitación a modificar.
        :param libre: Almacena el estado al que pasará la habitación.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('UPDATE habitaciones SET libre = ? WHERE numero = ?',
                             (libre, nhab))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def comprobardisponibilidad(nhab):
    try:
        conexion.cur.execute('SELECT libre FROM habitaciones WHERE numero = ?', (nhab,))
        libre = conexion.cur.fetchone()
        if libre[0] == 'Si':
            return True
        else:
            return False
    except:
        print("Error comprobando disponibilidad")
