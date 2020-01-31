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
        variables.precios[0].set_text(str(precios[0][0]))
        variables.precios[1].set_text(str(precios[0][1]))
        variables.precios[2].set_text(str(precios[0][2]))
    except:
        print("No hay precios guardados")
        conexion.cur.execute("INSERT INTO precios (preciopar, preciodes, preciocom) VALUES (0,0,0)")
        conexion.conex.commit()

def guardar_precio(precios):
    try:
        conexion.cur.execute('UPDATE precios SET preciopar = ?, preciodes = ?, preciocom = ?',
                             (str(precios[0].get_text()), str(precios[1].get_text()), str(precios[2].get_text())))
        conexion.conex.commit()
        print("Precios guardados")
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    try:
        codres = variables.reserva_seleccionada
        conexion.cur.execute('SELECT codser, tipo, precio FROM servicios WHERE codres = ?', (codres,))
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#esta función carga el treeview con los datos de la tabla servicios
def listadoser(listservicios):
    try:
        variables.listadoser = listar()
        listservicios.clear()
        for registro in variables.listadoser:
            listservicios.append(registro)
    except:
        print('Error en cargar treeview')

def insertarser(fila):
    try:
        conexion.cur.execute("INSERT INTO servicios (codres, tipo, precio) VALUES (?,?,?)", fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()