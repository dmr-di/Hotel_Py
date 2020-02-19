#coding=utf-8

"""Módulo que gestiona el pdf de la factura.

Contiene las siguientes funciones:

"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, shutil

import variables


def basico():
    """
    Crea la cabecera y el pie de la factura.
        :return: No retorna nada.

    """
    try:
        global bill
        bill = canvas.Canvas("Facturas/prueba.pdf", pagesize=A4)

        bill.setTitle("Factura prueba")

        text1 = "Bienvenido a nuestro hotel"
        bill.drawString(240, 780, "HOTEL LITE")
        bill.drawImage("./img/hotel.png", 475, 680, width=64, height=64)
        #bill.line(50, 670, 540, 670)

        bill.setFont("Times-Italic", size=8)
        bill.drawString(235, 765, text1)

        text2 = "CIF = 000000000A"
        bill.drawString(250, 755, text2)

        bill.line(50, 30, 540, 30)
        textpie = "Hotel Lite, CIF = 000000000A, Tlfn = 986000000, e-mail = info@hotellite.com"
        bill.drawString(280, 20, textpie)

    except:
        print("Error en básico")

def factura(datosfactura):
    """
    Crea los datos del cliente en la factura.
        :param datosfactura: Lista que almacena los datos del cliente y la reserva.
        :return: No retorna nada.

    """
    try:
        basico()
        bill.setFont('Helvetica-Bold', size=10)
        numfac = 'Nº de factura'
        bill.drawString(50, 725, numfac)
        bill.setFont('Helvetica', size=10)
        bill.drawString(140, 725, str(datosfactura[0]))

        bill.setFont('Helvetica-Bold', size=10)
        fechafac = 'Fecha Factura'
        bill.drawString(275, 725, fechafac)
        bill.setFont('Helvetica', size=10)
        bill.drawString(350, 725, str(datosfactura[1]))

        bill.setFont('Helvetica-Bold', size=10)
        dni = 'DNI'
        bill.drawString(50, 700, dni)
        bill.setFont('Helvetica', size=10)
        bill.drawString(140, 700, datosfactura[2])

        bill.setFont('Helvetica-Bold', size=10)
        numhab = 'Nº Habitación'
        bill.drawString(275, 700, numhab)
        bill.setFont('Helvetica', size=10)
        bill.drawString(350, 700, str(datosfactura[3]))

        bill.setFont('Helvetica-Bold', size=10)
        apel = 'Apelidos'
        bill.drawString(50, 675, apel)
        bill.setFont('Helvetica', size=10)
        bill.drawString(140, 675, str(datosfactura[4]))

        bill.setFont('Helvetica-Bold', size=10)
        nome = 'Nome'
        bill.drawString(275, 675, nome)
        bill.setFont('Helvetica', size=10)
        bill.drawString(350, 675, str(datosfactura[5]))

        servicios()

        total()

        bill.showPage()
        bill.save()
        dir = os.getcwd()
        os.system("/usr/bin/xdg-open " + dir + "/Facturas/prueba.pdf")
    except:
        print("Error en módulo factura")

def servicios():
    """
    Crea la tabla con los servicios en la factura.
        :return: No retorna nada.

    """
    try:
        CONCEPTO = 0
        UNIDADES = 1
        PRECIO = 2
        TOTAL = 3

        #Rectangulo
        bill.setFillColorRGB(1, 0.49, 0)
        bill.setStrokeColorRGB(1, 0.49, 0)
        bill.rect(40, 638, 500, 20, fill=True)
        bill.setFillColorRGB(0, 0, 0)
        bill.setStrokeColorRGB(0, 0, 0)

        # Concepto
        bill.setFont('Helvetica-Bold', size=10)
        concepto = 'CONCEPTO'
        x_conc = 50
        y_conc = 645
        bill.drawString(x_conc, y_conc, concepto)
        bill.setFont('Helvetica', size=10)
        y_conc -= 20
        bill.drawString(x_conc, y_conc, str(variables.servicio[CONCEPTO].get_text()))
        bill.setFont('Helvetica', size=10)
        for i in range(len(variables.grid_factura)):
            y_conc -= 20
            if variables.grid_factura[i][CONCEPTO].get_text() != "":
                bill.drawString(x_conc, y_conc, str(variables.grid_factura[i][CONCEPTO].get_text()))
                bill.setFont('Helvetica', size=10)

        # Unidades
        bill.setFont('Helvetica-Bold', size=10)
        unidad = 'UNIDADES'
        x_uni = 190
        y_uni = 645
        bill.drawCentredString(x_uni, y_uni, unidad)
        bill.setFont('Helvetica', size=10)
        y_uni -= 20
        bill.drawCentredString(x_uni, y_uni, str(variables.servicio[UNIDADES].get_text()))
        bill.setFont('Helvetica', size=10)
        for i in range(len(variables.grid_factura)):
            y_uni -= 20
            if variables.grid_factura[i][UNIDADES].get_text() != "":
                bill.drawCentredString(x_uni, y_uni, str(int(float(variables.grid_factura[i][UNIDADES].get_text()))))
                bill.setFont('Helvetica', size=10)

        # Precio
        bill.setFont('Helvetica-Bold', size=10)
        precio = 'PRECIO UNIDAD'
        x_prec = 355
        y_prec = 645
        bill.drawCentredString(x_prec, y_prec, precio)
        bill.setFont('Helvetica', size=10)
        y_prec -= 20
        bill.drawCentredString(x_prec, y_prec, str(variables.servicio[PRECIO].get_text() + "€"))
        bill.setFont('Helvetica', size=10)
        for i in range(len(variables.grid_factura)):
            y_prec -= 20
            if variables.grid_factura[i][PRECIO].get_text() != "":
                bill.drawCentredString(x_prec, y_prec, str(variables.grid_factura[i][PRECIO].get_text() + "€"))
                bill.setFont('Helvetica', size=10)

        # Total
        bill.setFont('Helvetica-Bold', size=10)
        total = 'TOTAL'
        x_total = 530
        y_total = 645
        bill.drawRightString(x_total, y_total, total)
        bill.setFont('Helvetica', size=10)
        y_total -= 20
        bill.drawRightString(x_total, y_total, str(variables.servicio[TOTAL].get_text() + "€"))
        bill.setFont('Helvetica', size=10)
        for i in range(len(variables.grid_factura)):
            y_total -= 20
            if variables.grid_factura[i][TOTAL].get_text() != "":
                bill.drawRightString(x_total, y_total, str(variables.grid_factura[i][TOTAL].get_text() + "€"))
                bill.setFont('Helvetica', size=10)

        # Separadores
        bill.setStrokeColorRGB(1, 0.49, 0)
        y_line = 620
        for i in range(len(variables.grid_factura)):
            if variables.grid_factura[i][0].get_text() != "":
                bill.line(40, y_line, 540, y_line)
                y_line -= 20
        bill.setStrokeColorRGB(0, 0, 0)

    except:
        print("Error cargando servicios")

def total():
    """
    Crea el apartado de total en la factura.
        :return: No retorna nada.

    """
    try:
        # Separador
        bill.line(50, 110, 540, 110)

        # Subtotal
        bill.setFont('Helvetica-Bold', size=12)
        subtotal = 'Subtotal:'
        bill.drawRightString(450, 90, subtotal)
        bill.setFont('Helvetica', size=10)
        bill.drawRightString(530, 90, variables.factura_total[0].get_text())

        # IVA
        bill.setFont('Helvetica-Bold', size=12)
        iva = 'IVA:'
        bill.drawRightString(450, 65, iva)
        bill.setFont('Helvetica', size=10)
        bill.drawRightString(530, 65, variables.factura_total[1].get_text())

        # Rectangulo
        bill.setFillColorRGB(1, 0.60, 0.20)
        bill.setStrokeColorRGB(1, 0.55, 0.15)
        bill.roundRect(400, 34, 140, 20, 10, fill=True)
        bill.setFillColorRGB(0, 0, 0)
        bill.setStrokeColorRGB(0, 0, 0)

        # Total
        bill.setFont('Helvetica-Bold', size=12)
        total = 'Total:'
        bill.drawRightString(450, 40, total)
        bill.setFont('Helvetica-Bold', size=10)
        bill.drawRightString(530, 40, variables.factura_total[2].get_text())

    except:
        print("Error cargando total")