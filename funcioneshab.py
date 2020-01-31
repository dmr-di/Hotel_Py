import sqlite3

import variables, conexion

def limpiarEntry(fila):
    for i in range(len(fila)):
        fila[i].set_text('')
    variables.switch.set_active(True)

def seleccionRB():
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
    try:
        if (variables.switch.get_active()):
            libre = 'Si'
        else:
            libre = 'No'
        return libre
    except:
        print("Error función switch")

def insertarhab(fila):
    try:
        conexion.cur.execute("INSERT INTO habitaciones (numero, tipo, precio, libre) VALUES (?,?,?,?)", fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#select para utilizar en las operaciones de datos
def listar():
    try:
        conexion.cur.execute('SELECT numero, tipo, precio, libre FROM habitaciones')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#esta función carga el treeview con los datos de la tabla clientes
def listadohab(listhabitaciones):
    try:
        variables.listadohab = listar()
        listhabitaciones.clear()
        for registro in variables.listadohab:
            listhabitaciones.append(registro)
    except:
        print('Error en cargar treeview')

#Esta función da de baja a una habitación
def bajahab(num):
    try:
        conexion.cur.execute('DELETE FROM habitaciones WHERE numero = ?', (num,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#Esta función modifica los datos de una habitación
def modifhab(registro):
    try:
        conexion.cur.execute('UPDATE habitaciones SET numero = ?, tipo = ?, precio = ?, libre = ? WHERE numero = ?', (registro[0], registro[1], registro[2], registro[3], registro[0]))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()