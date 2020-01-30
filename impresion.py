from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, shutil

def basico():
    try:
        global bill
        bill = canvas.Canvas("Facturas/prueba.pdf", pagesize=A4)

        bill.setTitle("Factura prueba")

        text1 = "Bienvenido a nuestro hotel"
        bill.drawString(240, 780, "HOTEL LITE")
        bill.drawImage("./img/hotel.png", 475, 680, width=64, height=64)
        bill.line(50, 670, 540, 670)

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

        bill.showPage()
        bill.save()
        dir = os.getcwd()
        os.system("/usr/bin/xdg-open " + dir + "/Facturas/prueba.pdf")
    except:
        print("Error en módulo factura")