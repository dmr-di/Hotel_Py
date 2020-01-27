import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import conexion, variables, funcionescli, funcioneshab, funcionesres, facturacion, impresion
import os, time, datetime, shutil
import xlrd, xlwt
from xlwt import *
from datetime import date

class Eventos():

    #Eventos generales

    def salir(self):
        conexion.Conexion().cerrarbbdd()
        Gtk.main_quit()

    def on_venPrincipal_destroy(self, widget):
        self.salir()

    def on_btnSalirtool_clicked(self, widget):
        self.salir()

    def on_btnSaliracercade_clicked(self, widget):
        variables.venacercade.hide()

    def on_btnSalirbackup_clicked(self, widget):
        variables.venfile.hide()

    def on_venFiledialog_selection_changed(self, widget):
        try:
            #este coge toda la ruta
            self.fichero =os.path.abspath(str(variables.venfile.get_filename()))
            self.fichero_nom = os.path.basename(str(variables.venfile.get_filename()))
            variables.lblfile.set_text("Fichero: " + self.fichero_nom)
            self.nombre = str(self.fichero_nom)
        except:
            print("error cogiendo fichero")

    def on_btnRestaurar_clicked(self, widget):
        try:
            ruta = "/home/a18danielmr/PycharmProjects/Empresa/" + self.nombre
            conexion.Conexion().cerrarbbdd()
            shutil.copy(self.fichero, ruta)
            os.remove("Empresa.sqlite")
            os.rename(self.nombre, "Empresa.sqlite")
            print("Base de datos restaurada correctamente")
            conexion.Conexion().abrirbbdd()
            variables.venfile.hide()
        except:
            print("Error restaurar bd")

    #Eventos clientes


    def on_btnAltacli_clicked(self, widget):
        try:
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            if funcionescli.comprobarDni(dni):
                registro = (dni, apel, nome, data)
                if dni != '' and apel != '':
                    funcionescli.insertarcli(registro)
                    funcionescli.listadocli(variables.listclientes)
                    funcionescli.limpiarEntry(variables.filacli)
                    variables.infocli.set_text("Alta realizada correctamente")
                    variables.fecha.set_text(data)
        except:
            print('Error alta cliente')

    def on_btnBajacli_clicked(self, widget):
        try:
            dni = variables.filacli[0].get_text()
            if dni != '':
                funcionescli.bajacli(dni)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarEntry(variables.filacli)
                variables.infocli.set_text("Baja realizada correctamente")
                variables.fecha.set_text("")
            else:
                print('falta dni')
        except:
            print('Error en boton baja cliente')

    def on_btnModifcli_clicked(self, widget):
        try:
            cod = variables.lblcodigo.get_text()
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if dni != '':
                funcionescli.modifcli(registro, cod)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarEntry(variables.filacli)
            else:
                print('falta dni')
        except:
            print('error en boton modificar cliente')

    def on_entDni_focus_out_event(self, widget, event):
        try:
            variables.infocli.set_text("")
            variables.fecha.set_text("")
            dni = variables.filacli[0].get_text()
            if funcionescli.comprobarDni(dni):
                variables.mensajerr.set_text("")
            else:
                variables.mensajerr.set_text('ERROR')
        except:
            print('Error en focus')

    def on_entDni_key_release_event(self, widget, event):
        try:
            dni = variables.filacli[0].get_text()
            if funcionescli.comprobarDni(dni):
                variables.mensajerr.set_text('')
        except:
            print('Error en keyrelease')

    def on_treeClientes_cursor_changed(self, widget):
        try:
            model, iter = variables.treeclientes.get_selection().get_selected()
            # model: es el modelo de la tabla de datos
            #iter: es el número que identifica a la fila que hemos marcado
            funcionescli.limpiarEntry(variables.filacli)
            funcionesres.limpiarLabel()
            variables.mensajerr.set_text("")
            if iter != None:
                sdni = model.get_value(iter, 0)
                sapel = model.get_value(iter, 1)
                snome = model.get_value(iter, 2)
                sdata = model.get_value(iter, 3)
                if sdata is None:
                    sdata = ("")
                cod = funcionescli.selectcli(sdni)
                variables.lblcodigo.set_text(str(cod[0]))
                variables.filacli[0].set_text(str(sdni))
                variables.filacli[1].set_text(str(sapel))
                variables.filacli[2].set_text(str(snome))
                variables.filacli[3].set_text(str(sdata))
                variables.lbldnires.set_text(str(sdni))
                variables.lblapelres.set_text(str(sapel))
        except:
            print("Error cargar cliente")

    def on_btnCalendar_clicked(self, widget):
        try:
            variables.llamada = 1
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print("Error abrir calendario")

    def on_Calendar_day_selected_double_click(self, widget):
        try:
            formato_fecha = "%d/%m/%Y"
            agno, mes, dia = variables.calendar.get_date()
            fecha = "%s/" % dia + "%s/" % (mes + 1) + "%s" % agno
            if variables.llamada == 1:
                variables.filacli[3].set_text(fecha)
            elif variables.llamada == 2:
                variables.filares[0].set_text(fecha)
            elif variables.llamada == 3:
                variables.filares[1].set_text(fecha)
            if variables.filares[0].get_text() != "" and variables.filares[1].get_text() != "":
                # Importante hay que llamar a datetime 2 veces
                variables.dia_entrada = datetime.datetime.strptime(variables.filares[0].get_text(), formato_fecha)
                variables.dia_salida = datetime.datetime.strptime(variables.filares[1].get_text(), formato_fecha)
                variables.lblnoches.set_text(str((variables.dia_salida-variables.dia_entrada).days))
            variables.vencalendar.hide()
        except:
            print('Error al coger la fecha')

    #Eventos Habitaciones

    def on_btnAltahab_clicked(self, widget):
        try:
            numero = variables.filahab[0].get_text()
            tipo = funcioneshab.seleccionRB()
            precio = variables.filahab[1].get_text()
            precio = float(precio.replace(',', '.'))
            precio = round(precio, 2)
            libre = funcioneshab.seleccionSwitch()
            registro = (numero, tipo, precio, libre)
            if numero != '' and tipo != '':
                funcioneshab.insertarhab(registro)
                funcioneshab.listadohab(variables.listhabitaciones)
                funcioneshab.limpiarEntry(variables.filahab)
                variables.infohab.set_text("Alta realizada correctamente")
                funcionesres.listadoreshab(variables.listreshab)
        except:
            print('Error alta habitacion')

    def on_treeHabitaciones_cursor_changed(self, widget):
        try:
            model, iter = variables.treehabitaciones.get_selection().get_selected()
            funcioneshab.limpiarEntry(variables.filahab)
            if iter != None:
                snum = model.get_value(iter, 0)
                stipo = model.get_value(iter, 1)
                sprecio = model.get_value(iter, 2)
                slibre = model.get_value(iter, 3)
                variables.filahab[0].set_text(str(snum))
                if stipo == str('Simple'):
                    variables.rbgrouphab[0].set_active(True)
                elif stipo == str('Doble'):
                    variables.rbgrouphab[1].set_active(True)
                elif stipo == str('Familiar'):
                    variables.rbgrouphab[2].set_active(True)
                sprecio = round(sprecio, 2)
                variables.filahab[1].set_text(str(sprecio))
                if slibre == 'Si':
                    variables.switch.set_active(True)
                else:
                    variables.switch.set_active(False)
        except:
            print('Error carga habitación')

    def on_btnBajahab_clicked(self, widget):
        try:
            num = variables.filahab[0].get_text()
            if num != '':
                funcioneshab.bajahab(num)
                funcioneshab.listadohab(variables.listhabitaciones)
                funcioneshab.limpiarEntry(variables.filahab)
                variables.infohab.set_text("Baja realizada correctamente")
                funcionesres.listadoreshab(variables.listreshab)
            else:
                print('falta numero')
        except:
            print('Error en boton baja habitación')

    def on_btnModifhab_clicked(self, widget):
        try:
            num = variables.filahab[0].get_text()
            tipo = funcioneshab.seleccionRB()
            precio = variables.filahab[1].get_text()
            if variables.switch.get_active():
                libre = 'Si'
            else:
                libre = 'No'
            registro = (num, tipo, precio, libre)
            if num != '':
                funcioneshab.modifhab(registro)
                funcioneshab.listadohab(variables.listhabitaciones)
                funcioneshab.limpiarEntry(variables.filahab)
            else:
                print('falta número')
        except:
            print('error en boton modificar habitación')

    #Eventos Reservas

    def on_btnCalendarin_clicked(self, widget):
        try:
            variables.llamada = 2
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print("Error abrir calendario")


    def on_btnCalendarout_clicked(self, widget):
        try:
            variables.llamada = 3
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print("Error abrir calendario")

    def on_btnAltares_clicked(self, widget):
        try:
            dni = variables.lbldnires.get_text()
            apel = variables.lblapelres.get_text()
            habitacion = variables.numhab
            chkin = variables.filares[0].get_text()
            chkout = variables.filares[1].get_text()
            registro = (dni, apel, habitacion, chkin, chkout)
            if dni != '' and apel != '' and habitacion != '' and chkin != '' and chkout != '':
                funcionesres.insertarres(registro)
                funcionesres.habocupada(habitacion, "No")
                funcioneshab.listadohab(variables.listhabitaciones)
                funcionesres.listadores(variables.listreservas)
                funcionesres.limpiarEntry(variables.filares)
                variables.infores.set_text("Alta realizada correctamente")
            else:
                variables.infores.set_text("Falta algún dato")
        except:
            print("Error alta reservas")

    def on_btnCout_clicked(self, widget):
        try:
            chkout = variables.filares[1].get_text()
            today = date.today()
            hoy = datetime.datetime.strftime(today, '%d/%m/%Y')
            if hoy > chkout:
                #TODO Puede facturar
                print("Factura OK")
            else:
                variables.infores.set_text("La fecha no puede ser inferior a la de hoy")
        except:
            print("Error en boton check-out")

    def on_btnBajares_clicked(self, widget):
        try:
            cod = variables.codreserva
            model = variables.cbreshab.get_model()
            nhab = model[variables.cbreshab.get_active_iter()][0]
            if cod != '':
                funcionesres.bajares(cod)
                funcionesres.listadores(variables.listreservas)
                funcionesres.limpiarEntry(variables.filares)
                funcionesres.habocupada(nhab, "Si")
                funcioneshab.listadohab(variables.listhabitaciones)
                variables.infores.set_text("Baja realizada correctamente")
            else:
                print('falta numero')
        except:
            print('Error en boton baja reservas')


    def on_btnModifres_clicked(self, widget):
        try:
            variables.modif = True
            formato_fecha = "%d/%m/%Y"
            cod = variables.codreserva
            dni = variables.lbldnires.get_text()
            apel = variables.lblapelres.get_text()
            habitacion = variables.numhab
            chkin = variables.filares[0].get_text()
            chkout = variables.filares[1].get_text()
            dia_entrada = datetime.datetime.strptime(chkin, formato_fecha)
            dia_salida = datetime.datetime.strptime(chkout, formato_fecha)
            variables.numnoches = str((dia_salida - dia_entrada).days)
            registro = (cod, dni, apel, habitacion, chkin, chkout)
            if cod != "":
                funcionesres.modifres(registro)
                funcionesres.listadores(variables.listreservas)
                funcionesres.limpiarEntry(variables.filares)
                reg_fac = (cod, dni, apel, habitacion, chkout)
                facturacion.cargar_datos(reg_fac)
                variables.modif = False
            else:
                print("No se encuentra el código")
        except:
            print("error en boton modificar reserva")

    def on_treeReservas_cursor_changed(self, widget):
        try:
            formato_fecha = "%d/%m/%Y"
            model, iter = variables.treereservas.get_selection().get_selected()
            funcionesres.limpiarEntry(variables.filares)
            if iter != None:
                variables.codreserva = model.get_value(iter, 0)
                sdni = model.get_value(iter, 1)
                sapel = model.get_value(iter, 2)
                shabitacion = model.get_value(iter, 3)
                schkin = model.get_value(iter, 4)
                schkout = model.get_value(iter, 5)
                variables.lbldnires.set_text(sdni)
                variables.lblapelres.set_text(sapel)
                nreg = funcionesres.selecregistro(shabitacion)
                variables.cbreshab.set_active(nreg[0]-1)
                variables.filares[0].set_text(schkin)
                variables.filares[1].set_text(schkout)
                dia_entrada = datetime.datetime.strptime(schkin, formato_fecha)
                dia_salida = datetime.datetime.strptime(schkout, formato_fecha)
                variables.lblnoches.set_text(str((dia_salida - dia_entrada).days))
                if variables.modif == False:
                    variables.numnoches = variables.lblnoches.get_text()
                    registro = (variables.codreserva, sdni, sapel, shabitacion, schkout)
                    facturacion.cargar_datos(registro)
                snome = facturacion.cargar_nombre(sdni)
                variables.datosfactura = (variables.codreserva, schkout, sdni, shabitacion, sapel, snome)
        except:
            print('Error carga reservas')


    #Eventos comboBox

    def on_cbReshab_changed(self, widget):
        try:
            index = variables.cbreshab.get_active()
            model = variables.cbreshab.get_model()
            item = model[index]
            variables.numhab = item[0]
        except:
            print("Error al coger numero habitacion comboBox")

    #Eventos Toolbar

    def on_btnClitool_clicked(self, widget):
        try:
            #Este método devuelve un entero con la posición del panel
            panelactual = variables.panel.get_current_page()
            if panelactual != 0:
                variables.panel.set_current_page(0)
            else:
                pass
        except:
            print("Error boton cliente toolbar")

    def on_btnReservastool_clicked(self, widget):
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 1:
                variables.panel.set_current_page(1)
            else:
                pass
        except:
            print("Error boton reservas toolbar")

    def on_btnHabitaciontool_clicked(self, widget):
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 2:
                variables.panel.set_current_page(2)
            else:
                pass
        except:
            print("Error boton habitaciones toolbar")

    def on_btnLimpiartool_clicked(self, widget):
        try:
            funcionescli.limpiarEntry(variables.filacli)
            funcioneshab.limpiarEntry(variables.filahab)
            funcionesres.limpiarEntry(variables.filares)
            funcionesres.limpiarLabel()
            facturacion.limpiarFactura(variables.factura)
        except:
            print("Error boton limpiar toolbar")


    def on_btnCalc_clicked(self, widget):
        try:
            os.system("gnome-calculator")
        except:
            print("Error en boton calculadora")

    #Eventos MenuBar

    def on_mbSalir_activate(self, widget):
        self.salir()

    def on_mbAcercade_activate(self, widget):
        variables.venacercade.connect('delete-event', lambda w, e: w.hide() or True)
        variables.venacercade.show()

    def on_mbBackup_activate(self, widget):
        # Comprueba si existe el directorio si no lo crea
        directorio = "./Backups"
        try:
            os.stat(directorio)
        except:
            os.mkdir(directorio)
        # Hace la copia de seguridad
        try:
            conexion.Conexion().cerrarbbdd()
            # El fichero zipeado contendra su nombre y el día en que se crea
            fecha = datetime.datetime.now()
            shutil.copy("Empresa.sqlite", "Backups/" + str(fecha) + "_Backup_Empresa.sqlite")
            print("***Fichero copiado correctamente***")
            conexion.Conexion().abrirbbdd()
            variables.venfile.hide()
        except:
            print("Error backup")

    def on_mbImportar_activate(self, widget):
        document = xlrd.open_workbook("./datos/listadoclientes.xlsx")
        clientes = document.sheet_by_index(0)
        #Leemos el número de filas y columnas de la hoja de clientes
        filas_clientes = clientes.nrows
        columnas_clientes = clientes.ncols
        for i in range (1, clientes.nrows):
            fila = clientes.row_values(i)
            for j in range(len(fila)):
                if j == 3:
                    serial = fila[j]
                    seconds = (serial - 25569) * 86400.0
                    fecha = datetime.datetime.utcfromtimestamp(seconds)
                    fecha = fecha.strftime("%d/%m/%y")
                    fila[j] = fecha
            funcionescli.importarcli(fila)
        funcionescli.listadocli(variables.listclientes)
        variables.infocli.set_text("Importación realizada correctamente")

    def on_mbExportar_activate(self, widget):
        #Definicion de estilos
        style0 = xlwt.easyxf("font: name Times New Roman, colour red, bold on")
        #style1 = xlwt.easyxf("num_format_str='DD-MMM-YY'")
        style1 = XFStyle()
        style1.num_format_str = 'DD-MMM-YY'
        #Creamos el fichero excel
        wb = xlwt.Workbook()
        #le añadimos una hoja llamada NuevoClientes que permite sobreescribir celdas
        ws = wb.add_sheet("NuevoClientes", cell_overwrite_ok=True)
        ws.write(0,0,"DNI",style0)
        ws.write(0,1,"APELIDOS",style0)
        ws.write(0, 2, "NOMBRE", style0)
        ws.write(0, 3, "FECHA ALTA", style0)
        #Aquí consultamos un listado de clientes de la base de datos
        listado = funcionescli.listar()
        #Aqui recorremos el listado e insertamos en la celda correspondiente
        for registro in listado:
            i = listado.index(registro)
            for dato in registro:
                j = registro.index(dato)
                ws.write(i,j,dato,style1)
        #Guardamos la hoja de cálculo
        wb.save("./datos/ejemplo.xls")
        variables.infocli.set_text("Exportación realizada correctamente")


    def on_mbAbrir_activate(self, widget):
        variables.venfile.connect('delete-event', lambda w, e: w.hide() or True)
        variables.venfile.show()

    #Eventos impresion

    def on_btnImprimi_clicked(self, widget):
        try:
            impresion.factura(variables.datosfactura)
        except:
            print("Error en módulo impresión")