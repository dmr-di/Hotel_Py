import conexion, variables
import sqlite3

import funcionesser


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
    variables.servicio[1].set_text(variables.numnoches)
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

def calcular_total():
    try:
        subtotal = 0
        iva = 0
        subtotal = subtotal + float(variables.servicio[3].get_text())
        iva = iva + (float(variables.servicio[3].get_text())*0.1)
        for i in range(len(variables.grid_factura)):
            if variables.grid_factura[i][0].get_text() != '':
                concepto = variables.grid_factura[i][0].get_text()
                precio = float(variables.grid_factura[i][3].get_text())
                subtotal = subtotal + float(precio)
                if (concepto == 'Desayuno' or concepto == 'Comida' or concepto == 'Parking'):
                    iva = iva + (float(precio)*0.1)
                else:
                    iva = iva + (float(precio)*0.21)
        variables.factura_total[0].set_text(str(round(subtotal, 2)) + "€")
        variables.factura_total[1].set_text(str(round(iva, 2)) + "€")
        variables.factura_total[2].set_text(str(round(subtotal+iva, 2)) + "€")
    except:
        print("Error calculando el total")

def limpiarFactura(factura):
    try:
        for i in range(len(factura)):
            factura[i].set_text("")
        for i in range(len(variables.servicio)):
            variables.servicio[i].set_text("")
        for i in range(len(variables.factura_total)):
            variables.factura_total[i].set_text("")
    except:
        print("error limpiando factura")
