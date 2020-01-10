import conexion, variables
import sqlite3

def cargar_datos(registro):
    variables.factura[0].set_text(str(registro[0]))
    variables.factura[1].set_text(str(registro[1]))
    variables.factura[2].set_text(str(registro[2]))
    variables.factura[3].set_text(str(cargar_nombre(registro[1])))
    variables.factura[4].set_text(str(registro[3]))
    variables.factura[5].set_text(str(cargar_tipo(registro[3])))
    variables.factura[6].set_text(str(registro[4]))
    mostrar_cargos(variables.factura)

def mostrar_cargos(factura):
    variables.servicio[0].set_text("Noches")
    variables.servicio[1].set_text(variables.lblnoches.get_text())
    precio = cargar_precio(factura[4].get_text())
    variables.servicio[2].set_text(str(precio))
    total = precio*float(variables.servicio[1].get_text())
    variables.servicio[3].set_text(str(round(total, 2)))

def cargar_precio(nhab):
    try:
        conexion.cur.execute('SELECT precio FROM habitaciones WHERE numero = ?', (nhab,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado[0]
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def cargar_nombre(dni):
    try:
        conexion.cur.execute('SELECT nome FROM clientes WHERE dni = ?', (dni,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado[0]
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def cargar_tipo(nhab):
    try:
        conexion.cur.execute('SELECT tipo FROM habitaciones WHERE numero = ?', (nhab,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado[0]
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiarFactura(factura):
    try:
        factura[0].set_text("")
        factura[1].set_text("")
        factura[2].set_text("")
        factura[3].set_text("")
        factura[4].set_text("")
        factura[5].set_text("")
        factura[6].set_text("")
    except:
        print("error limpiando factura")
