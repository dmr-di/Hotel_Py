import sqlite3

import variables, conexion

def limpiarEntry(fila):
    for i in range(len(fila)):
        fila[i].set_text('')

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

def insertarhab(fila):
    try:
        conexion.cur.execute("INSERT INTO habitaciones (numero, tipo, precio) VALUES (?,?,?)", fila[0], fila[1], float(fila[2]))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#select para utilizar en las operaciones de datos
def listar():
    try:
        conexion.cur.execute('SELECT numero, tipo, precio FROM habitaciones')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#esta función carga el treeview con los datos de la tabla clientes
def listadohab(listhabitaciones):
    try:
        variables.listado = listar()
        listhabitaciones.clear()
        for registro in variables.listado:
            listhabitaciones.append(registro)
    except:
        print('Error en cargar treeview')