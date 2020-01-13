from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

def basico():
    try:
        bill = canvas.Canvas("prueba.pdf", pagesize=A4)
        text1 = "Bienvenido a nuestro hotel"
        text2 = "CIF = 000000000A"
        bill.setFont("Helvetica-Bold", size=16)
        bill.drawImage("./img/hotel.png", 475, 680, width=64, height=64)
        bill.drawString(240, 780, "HOTEL LITE")
        bill.setFont("Times-Italic", size=10)
        bill.drawString(235, 765, text1)
        bill.drawString(250, 755, text2)
        bill.line(50, 670, 540, 670)
        textpie = "Hotel Lite, CIF = 000000000A, Tlfn = 986000000, e-mail = info@hotellite.com"
        bill.setFont("Times-Italic", size=8)
        bill.drawString(280, 20, textpie)
        bill.line(50, 30, 540, 30)
        return bill
    except:
        print("Error en básico")

def factura():
    try:
        bill = basico()
        bill.showPage()
        bill.save()
        dir = os.getcwd()
        os.system("/usr/bin/xdg-open " + dir + "/prueba.pdf")
    except:
        print("Error en módulo factura")