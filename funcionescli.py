#coding=utf-8
""" Módulo que gestiona los clientes.

Este módulo contiene las funciones siguientes:

"""

import conexion, variables
import sqlite3

def limpiarEntry(fila):
    """
    Limpia la pestaña de clientes.
        :param fila: Listado que contiene los widgets de cliente que vamos a limpiar tras ejecutar un evento.
        :return: No retorna nada.

    """
    variables.lblcodigo.set_text("")
    for i in range(len(fila)):
        fila[i].set_text('')
    listadocli(variables.listclientes)

def comprobarDni(dni):
    """
    Comprueba si el dni introducido es correcto.
        :param dni: Contiene un dni recibido a través de un entry.
        :return: Retorna un booleano tras comprobar si el dni es válido.

    """
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if len(dni) == len([n for n in dni if n in numeros]):
            if tabla[int(dni) % 23] == dig_control:
                return True
    return False

def insertarcli(fila):
    """
    Inserta los datos de un cliente en la base de datos.
        :param fila: Listado que contiene los campos a insertar en la base de datos.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute("INSERT INTO clientes (dni, apel, nome, data) VALUES (?,?,?,?)", fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def importarcli(fila):
    """
    Importa los datos de varios clientes desde un archivo .csv.
        :param fila: Listado que contiene los datos de los clientes.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute("INSERT OR IGNORE INTO clientes (dni, apel, nome, data) VALUES (?,?,?,?)", (str(fila[0]), str(fila[1]), str(fila[2]), str(fila[3])))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#select para utilizar en las operaciones de datos
def listar():
    """
    Lista los clientes existentes en la base de datos para cargar el treeview.
        :return: Retorna el listado con todos los clientes.

    """
    try:
        conexion.cur.execute('SELECT dni, apel, nome, data FROM clientes')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def bajacli(dni):
    """
    Borra los datos de un cliente en la base de datos.
        :param dni: Contiene el dni del cliente que se quiere borrar.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('DELETE FROM clientes WHERE dni = ?', (dni,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def modifcli(registro, cod):
    """
    Modifica los datos de un cliente.
        :param registro: Registro con los datos modificados del cliente.
        :param cod: Codigo que identifica el cliente que se quiere modificar.
        :return: No retorna nada.

    """
    try:
        conexion.cur.execute('UPDATE clientes SET dni = ?, apel = ?, nome = ?, data = ? WHERE id = ?', (registro[0], registro[1], registro[2], registro[3], cod))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadocli(listclientes):
    """
    Carga el treeview con los datos de todos los clientes.
        :param listclientes: Listado que contiene los datos de todos los clientes.
        :return: No retorna nada.

    """
    try:
        variables.listadocli = listar()
        listclientes.clear()
        for registro in variables.listadocli:
            listclientes.append(registro)
    except:
        print('Error en cargar treeview')

def selectcli(dni):
    """
    Carga el id interno de un cliente.
        :param dni: Contiene el dni del cliente del cual queremos obtener su id.
        :return: Retorna el id del cliente

    """
    try:
        conexion.cur.execute('SELECT id FROM clientes WHERE dni = ?', (dni,))
        cod = conexion.cur.fetchone()
        return cod
    except:
        print('Error selectcli')
