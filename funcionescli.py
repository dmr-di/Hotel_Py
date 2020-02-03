""" Módulo que gestiona los clientes

Este módulo contiene las funciones siguientes
* limpiarentry
    - :fila: contiene un listado de widgets de cliente que vamos a limpiar tras ejecutar un evento
    return: no devuelve nada
* comprobarDNI
    - :fila: contiene un dni recibido a través de un entry
    return: devuelve un booleano tras comprobar si el dni es válido

"""

import conexion, variables
import sqlite3

def limpiarEntry(fila):
    variables.lblcodigo.set_text("")
    for i in range(len(fila)):
        fila[i].set_text('')

def comprobarDni(dni):
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

#inserta un registro
def insertarcli(fila):
    try:
        conexion.cur.execute("INSERT INTO clientes (dni, apel, nome, data) VALUES (?,?,?,?)", fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def importarcli(fila):
    try:
        conexion.cur.execute("INSERT OR IGNORE INTO clientes (dni, apel, nome, data) VALUES (?,?,?,?)", (str(fila[0]), str(fila[1]), str(fila[2]), str(fila[3])))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#select para utilizar en las operaciones de datos
def listar():
    try:
        conexion.cur.execute('SELECT dni, apel, nome, data FROM clientes')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#Esta función da de baja a un cliente
def bajacli(dni):
    try:
        conexion.cur.execute('DELETE FROM clientes WHERE dni = ?', (dni,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


#Esta función modifica los datos de un cliente
def modifcli(registro, cod):
    try:
        conexion.cur.execute('UPDATE clientes SET dni = ?, apel = ?, nome = ?, data = ? WHERE id = ?', (registro[0], registro[1], registro[2], registro[3], cod))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#esta función carga el treeview con los datos de la tabla clientes
def listadocli(listclientes):
    try:
        variables.listadocli = listar()
        listclientes.clear()
        for registro in variables.listadocli:
            listclientes.append(registro)
    except:
        print('Error en cargar treeview')

def selectcli(dni):
    try:
        conexion.cur.execute('SELECT id FROM clientes WHERE dni = ?', (dni,))
        cod = conexion.cur.fetchone()
        return cod
    except:
        print('Error selectcli')
