#coding=utf-8

"""Módulo que gestiona los servicios.

Contiene las siguientes funciones:

"""

import sqlite3

import variables, conexion, facturacion

def limpiar():
    """
    Limpia los widgets de la pestaña de servicios.
        :return: No retorna nada.

    """
    variables.rgservicios[0].set_active(True)
    variables.cbparking.set_active(False)
    for i in range(len(variables.entser_adicionales)):
        variables.entser_adicionales[i].set_text("")

def cargar_precios():
    """
    Carga los precios de los servicios básicos.
        :return: Retorna una lista con todos los precios.

    """
    try:
        conexion.cur.execute('SELECT * FROM precios')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar_precios():
    """
    Muestra los precios en su widget correspondiente.
        :return: No retorna nada.
        :except: Si no hay precios registrados los inicia a 0 en la base de datos.

    """
    try:
        precios = cargar_precios()
        variables.precios[0].set_text(str(precios[0][0]))
        variables.precios[1].set_text(str(precios[0][1]))
        variables.precios[2].set_text(str(precios[0][2]))
    except:
        print("No hay precios guardados")
        conexion.cur.execute("INSERT INTO precios (preciopar, preciodes, preciocom) VALUES (0,0,0)")
        conexion.conex.commit()

def guardar_precio(precios):
    """
    Registra los nuevos precios en la base de datos.
        :param precios: Lista que contiene los precios modificados.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('UPDATE precios SET preciopar = ?, preciodes = ?, preciocom = ?',
                             (str(precios[0].get_text()), str(precios[1].get_text()), str(precios[2].get_text())))
        conexion.conex.commit()
        print("Precios guardados")
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    """
    Carga los datos de los servicios registradas en una lista.
        :return: Retorna la lista con todas los servicios.

    """
    try:
        codres = variables.reserva_seleccionada
        conexion.cur.execute('SELECT codser, tipo, precio FROM servicios WHERE codres = ?', (codres,))
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadoser(listservicios):
    """
    Carga el treeview con todos los servicios registrados.
        :param listservicios: Almacena el treeview de servicios.
        :return: No retorna nada.

    """
    try:
        variables.listadoser = listar()
        listservicios.clear()
        for registro in variables.listadoser:
            listservicios.append(registro)
    except:
        print('Error en cargar treeview')

def insertarser(fila):
    """
    Realiza una inserción de un servicio en la base de datos.
        :param fila: Lista que almacena los datos de un servicio.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute("INSERT INTO servicios (codres, tipo, precio) VALUES (?,?,?)", fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def bajaser(fila):
    """
    Realiza un borrado de un servicio en la base de datos.
        :param fila: Lista que almacena el código del servicio y el de la reserva.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('DELETE FROM servicios WHERE codser = ? and codres = ?', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiar_factura():
    """
    Limpia los labels correspondientes a los servicios extra.
        :return: No retorna nada.

    """
    for i in range(len(variables.grid_factura)):
        for j in range(len(variables.grid_factura[i])):
            variables.grid_factura[i][j].set_text("")

def cargar_factura():
    """
    Carga la factura con los servicios extra.
        :return: No retorna nada.

    """
    limpiar_factura()
    registro = listar()
    unidad = float(variables.servicio[1].get_text())
    for i in range(len(registro)):
        concepto = registro[i][1]
        precio = registro[i][2]
        variables.grid_factura[i][0].set_text(concepto)
        if (concepto == 'Desayuno' or concepto == 'Comida' or concepto == 'Parking'):
            total = unidad * precio
            variables.grid_factura[i][1].set_text(str(unidad))
            variables.grid_factura[i][2].set_text(str(precio))
            variables.grid_factura[i][3].set_text(str(total))
        else:
            total = precio
            variables.grid_factura[i][1].set_text(str(1))
            variables.grid_factura[i][2].set_text(str(precio))
            variables.grid_factura[i][3].set_text(str(total))
    facturacion.calcular_total()