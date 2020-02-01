import sqlite3

import variables, conexion

def limpiar():
    variables.rgservicios[0].set_active(True)
    variables.cbparking.set_active(False)
    for i in range(len(variables.entser_adicionales)):
        variables.entser_adicionales[i].set_text("")

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

def bajaser(fila):
    try:
        conexion.cur.execute('DELETE FROM servicios WHERE codser = ? and codres = ?', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiar_factura():
    for i in range(len(variables.grid_factura)):
        for j in range(len(variables.grid_factura[i])):
            variables.grid_factura[i][j].set_text("")

def cargar_factura():
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