from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

def basico():
    try:
        bill = canvas.Canvas("prueba.pdf", pagesize=A4)
        text1 = "Bienvenido a nuestro hotel"
        bill.setFont("Helvetica-Bold", size=16)
        bill.drawImage("./img/hotel.png", 475, 680, width=64, height=64)
        bill.drawString(240, 780, "HOTEL LITE")
        bill.setFont("Times-Italic", size=10)
        bill.drawString(235, 765, text1)
        bill.line(50, 670,540,670)
        bill.showPage()
        bill.save()
        dir = os.getcwd()
        os.system("/usr/bin/xdg-open " + dir + "/prueba.pdf")
    except:
        print("Error en básico")

def factura():
    try:
        basico()
    except:
        print("Error en módulo factura")