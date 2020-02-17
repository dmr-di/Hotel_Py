# coding=utf-8

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import conexion, variables, funcionescli, funcioneshab, funcionesres, funcionesser, facturacion, impresion
import os, datetime, shutil
#import xlrd, xlwt
from xlwt import *
from datetime import date


class Eventos():
    """ Módulo que gestiona los eventos de la aplicación

    Contiene las siguientes funciones:

    """

    # Eventos generales

    def salir(self):
        """
        Cierra la conexión con la base de datos y la aplicación.
            :return: No retorna nada.

        """
        conexion.Conexion().cerrarbbdd()
        Gtk.main_quit()

    def on_venPrincipal_destroy(self, widget):
        """
        Gestiona la "destrucción" de la ventana principal.
            :param widget: Contiene el widget de la ventana.
            :return: No retorna nada.

        """
        self.salir()

    def on_btnSaliracercade_clicked(self, widget):
        """
        Esconde la ventana de información "Acerca de".
            :param widget: Contiene el widget de la ventana.
            :return: No retorna nada.

        """
        variables.venacercade.hide()

    def on_btnSalirbackup_clicked(self, widget):
        """
        Esconde la ventana de elección de fichero para backup.
            :param widget: Contiene el widget de la ventana.
            :return: No retorna nada.

        """
        variables.venfile.hide()

    def on_venFiledialog_selection_changed(self, widget):
        """
        Controla la selección en la ventana de selección de fichero.
            :param widget: Contiene el widget de la ventana.
            :return: No retorna nada.

        """
        try:
            # este coge toda la ruta
            self.fichero = os.path.abspath(str(variables.venfile.get_filename()))
            self.fichero_nom = os.path.basename(str(variables.venfile.get_filename()))
            variables.lblfile.set_text("Fichero: " + self.fichero_nom)
            self.nombre = str(self.fichero_nom)
        except:
            print("error cogiendo fichero")

    def on_btnRestaurar_clicked(self, widget):
        """
        Gestiona el click en el botón de restaurar, esconde la ventana de selección
        de fichero y carga el backup de la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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

    # Eventos ventana salir
    def on_venSalir_destroy(self, widget):
        """
        Esconde la ventana de dialogo que permite salir de la aplicación.
            :param widget: Contiene el widget de la ventana
            :return: No retorna nada.

        """
        variables.vensalir.hide()

    def on_btnAceptar_clicked(self, widget):
        """
        Gestiona el click del botón "Aceptar" de la ventana de dialogo, cierra la app cuando se hace click.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        self.salir()

    def on_btnCancelar_clicked(self, widget):
        """
        Gestiona el click del botón "Cancelar" de la ventana de dialogo, cancela la acción de salir
        y esconde la ventana de dialogo.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        variables.vensalir.hide()

    # Eventos clientes

    def on_btnAltacli_clicked(self, widget):
        """
        Gestiona el click del botón de "Alta" de la pestaña de clientes.
        Recoge los datos del cliente y los guarda en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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
        """
        Gestiona el click del botón de "Baja" de la pestaña de clientes.
        Recoge el dni del cliente y lo borra de la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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
        """
        Gestiona el click del botón "Modificar" de la pestaña de clientes.
        Recoge los nuevos datos del cliente y lo modifica en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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
        """
        Gestiona el evento que ocurre al desmarcar el entry de dni del cliente.
        Comprueba si el dni es correcto y si no lo es lanza un mensaje de error.
            :param widget: Contiene el widget del entry.
            :param event: Contiene la referencia al evento.
            :return: No retorna nada.

        """
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
        """
        Gestiona el evento que ocurre al pulsar cualquier tecla en el entry de dni del cliente.
        Comprueba si el dni es correcto y si no lo es lanza un mensaje de error.
            :param widget: Contiene el widget del entry.
            :param event: Contiene la referencia al evento.
            :return: No retorna nada.

        """
        try:
            dni = variables.filacli[0].get_text()
            if funcionescli.comprobarDni(dni):
                variables.mensajerr.set_text('')
        except:
            print('Error en keyrelease')

    def on_treeClientes_cursor_changed(self, widget):
        """
        Gestiona el click en los registros del treeview de clientes.
        Recoge los datos del registro y los muestra en la aplicación.
            :param widget: Contiene el widget del treeview de cliente.
            :return: No retorna nada.

        """
        try:
            model, iter = variables.treeclientes.get_selection().get_selected()
            # model: es el modelo de la tabla de datos
            # iter: es el número que identifica a la fila que hemos marcado
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
        """
        Gestiona el click del botón de calendario.
        Lanza una ventana con un calendario que permite escoger una fecha.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            variables.llamada = 1
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print("Error abrir calendario")

    def on_Calendar_day_selected_double_click(self, widget):
        """
        Gestiona el doble click en un día concreto del calendario.
        Esconde la ventana y escribe la fecha seleccionada en su entry correspondiente.
            :param widget: Contiene el widget de la ventana.
            :return: No retorna nada.

        """
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
                variables.lblnoches.set_text(str((variables.dia_salida - variables.dia_entrada).days))
            variables.vencalendar.hide()
        except:
            print('Error al coger la fecha')

    # Eventos Habitaciones

    def on_btnAltahab_clicked(self, widget):
        """
        Gestiona el botón de "Alta" de la pestaña de habitaciones.
        Recoge los datos de la habitación y la inserta en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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
        """
        Gestiona el click en los registros del treeview de habitaciones.
        Recoge los datos del registro y los muestra en la aplicación.
            :param widget: Contiene el treeview de habitaciones.
            :return: No retorna nada.

        """
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
        """
        Gestiona el botón de "Baja" de la pestaña de habitaciones.
        Recoge el número de la habitación seleccionada y la elimina de la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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
        """
        Gestiona el botón de "Modificar" de la pestaña de habitaciones.
        Recoge los nuevos datos de la habitación y realiza un "update" en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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

    # Eventos Reservas

    def on_btnCalendarin_clicked(self, widget):
        """
        Gestiona un botón de llamada a la ventana de calendario para recoger la fecha de entrada.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            variables.llamada = 2
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print("Error abrir calendario")

    def on_btnCalendarout_clicked(self, widget):
        """
        Gestiona un botón de llamada a la ventana de calendario para recoger la fecha de salida.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            variables.llamada = 3
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print("Error abrir calendario")

    def on_btnAltares_clicked(self, widget):
        """
        Gestiona el botón de "Alta" de la pestaña de reservas.
        Recoge los datos de la reserva y realiza una inserción en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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
        """
        Comprueba las fechas de la reserva para ver si se puede realizar el check-out.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            chkout = variables.filares[1].get_text()
            today = date.today()
            hoy = datetime.datetime.strftime(today, '%d/%m/%Y')
            if hoy > chkout:
                print("Factura OK")
            else:
                variables.infores.set_text("La fecha no puede ser inferior a la de hoy")
        except:
            print("Error en boton check-out")

    def on_btnBajares_clicked(self, widget):
        """
        Contiene el botón de "Baja" de la pestaña de reservas.
        Recoge el código de la reserva seleccionada y realiza un borrado en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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
        """
        Contiene el botón de "Modificar" de la pestaña de reservas.
        Recoge los nuevos datos de la reserva y realiza un "update" en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
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
        """
        Gestiona el click en los registros del treeview de reservas.
        Recoge los datos del registro y los muestra en la aplicación.
            :param widget: Contiene el widget del treeview de reservas.
            :return: No retorna nada.

        """
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
                variables.cbreshab.set_active(nreg[0] - 1)
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
                variables.datos_servicio[0].set_text(str(variables.codreserva))
                variables.datos_servicio[1].set_text(str(shabitacion))

                # Cargo el treeServicios
                variables.reserva_seleccionada = model.get_value(iter, 0)
                funcionesser.listadoser(variables.listservicios)

                # Cargo la factura
                funcionesser.cargar_factura()
        except:
            print('Error carga reservas')

    # Eventos Servicios

    def on_rbOtro_toggled(self, widget):
        """
        Comprueba si el radiobutton esta seleccionado, en caso afirmativo muestra los campos
        de entrada de servicios adicionales.
            :param widget: Contiene el widget del radiobutton "Otro" de la pestaña de servicios.
            :return: No retorna nada.

        """
        try:
            if (variables.rgservicios[2].get_active()):
                for i in range(len(variables.servicios_adicionales)):
                    variables.servicios_adicionales[i].set_visible(True)
            else:
                for i in range(len(variables.servicios_adicionales)):
                    variables.servicios_adicionales[i].set_visible(False)
        except:
            print("Error en radiogroup servicios")

    def on_btnAltaSer_clicked(self, widget):
        """
        Contiene el botón de "Alta" de la pestaña de servicios.
        Comprueba el radiobutton seleccionado y carga los datos de la tabla precios de la base de datos.
        Si el radiobutton activo es "Otro" carga los datos de los entries de servicios adicionales.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            precios = funcionesser.cargar_precios()
            codres = variables.datos_servicio[0].get_text()
            if variables.rgservicios[0].get_active():
                concepto = "Desayuno"
                precio = precios[0][0]
            elif variables.rgservicios[1].get_active():
                concepto = "Comida"
                precio = precios[0][1]
            elif variables.rgservicios[2].get_active():
                concepto = variables.entser_adicionales[0].get_text()
                precio = variables.entser_adicionales[1].get_text()
            precio = float(precio.replace(',', '.'))
            precio = round(precio, 2)
            registro = (codres, str(concepto), precio)
            # Guardo el servicio en la bd
            funcionesser.insertarser(registro)
            if variables.cbparking.get_active():
                concepto = "Parking"
                precio = precios[0][2]
                precio = float(precio.replace(',', '.'))
                precio = round(precio, 2)
                registro = (codres, str(concepto), precio)
                funcionesser.insertarser(registro)
            funcionesser.listadoser(variables.listservicios)
            funcionesser.cargar_factura()
            funcionesser.limpiar()
        except:
            print("Error alta servicio")

    def on_btnBajaSer_clicked(self, widget):
        """
        Contiene el botón de "Baja" de la pestaña de servicios.
        Recoge el código de reserva y el código de servicio y realiza un borrado en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            codres = variables.datos_servicio[0].get_text()
            registro = (variables.codser, codres)
            funcionesser.bajaser(registro)
            funcionesser.listadoser(variables.listservicios)
            funcionesser.cargar_factura()
        except:
            print("Error baja servicio")

    def on_treeServicios_cursor_changed(self, widget):
        """
        Gestiona el click en el treeview de servicios.
        Guarda internamente el código del servicio seleccionado.
            :param widget: Contiene el widget del treeview de servicios.
            :return: No retorna nada.

        """
        try:
            model, iter = variables.treeservicios.get_selection().get_selected()
            if iter != None:
                variables.codser = model.get_value(iter, 0)
        except:
            print("Error carga servicios")

    # Eventos comboBox

    def on_cbReshab_changed(self, widget):
        """
        Gestiona la selección en el combobox que lista los números de las habitaciones.
        Guarda internamente el número de la habitación seleccionada.
            :param widget: Contiene el widget del combobox de habitaciones.
            :return: No retorna nada.

        """
        try:
            index = variables.cbreshab.get_active()
            model = variables.cbreshab.get_model()
            item = model[index]
            variables.numhab = item[0]
        except:
            print("Error al coger numero habitacion comboBox")

    # Eventos Toolbar

    def on_btnClitool_clicked(self, widget):
        """
        Gestiona el botón "Cliente" de la toolbar.
        Cambia la pestaña a la pestaña de clientes.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            # Este método devuelve un entero con la posición del panel
            panelactual = variables.panel.get_current_page()
            if panelactual != 0:
                variables.panel.set_current_page(0)
            else:
                pass
        except:
            print("Error boton cliente toolbar")

    def on_btnReservastool_clicked(self, widget):
        """
        Gestiona el botón "Reservas" de la toolbar.
        Cambia la pestaña a la pestaña de reservas.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 1:
                variables.panel.set_current_page(1)
            else:
                pass
        except:
            print("Error boton reservas toolbar")

    def on_btnHabitaciontool_clicked(self, widget):
        """
        Gestiona el botón "Habitación" de la toolbar.
        Cambia la pestaña a la pestaña de habitaciones.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 2:
                variables.panel.set_current_page(2)
            else:
                pass
        except:
            print("Error boton habitaciones toolbar")

    def on_btnLimpiartool_clicked(self, widget):
        """
        Gestiona el botón "Limpiar" de la toolbar.
        Vacia todos los entries de la aplicación y recarga sus treeviews.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            funcionescli.limpiarEntry(variables.filacli)
            funcioneshab.limpiarEntry(variables.filahab)
            funcionesres.limpiarEntry(variables.filares)
            funcionesres.limpiarLabel()
            facturacion.limpiarFactura(variables.factura)
            funcionesser.limpiar()
            funcionesser.limpiar_factura()
            funcionesser.limpiar_codres()
            variables.listservicios.clear()
        except:
            print("Error boton limpiar toolbar")

    def on_btnCalc_clicked(self, widget):
        """
        Gestiona el botón "Calculadora" de la toolbar.
        Abre la calculadora de Ubuntu.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            os.system("gnome-calculator")
        except:
            print("Error en boton calculadora")

    def on_btnImprimir_clicked(self, widget):
        """
        Gestiona el botón "Imprimir" de la toolbar.
        Muestra la factura en formato '.pdf'.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            impresion.factura(variables.datosfactura)
        except:
            print("Error en módulo impresión")

    def on_btnSalirtool_clicked(self, widget):
        """
        Gestiona el botón "Salir" de la toolbar.
        Cierra la aplicación preguntando antes al usuario.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        variables.vensalir.connect('delete-event', lambda w, e: w.hide() or True)
        variables.vensalir.show()

    # Eventos MenuBar

    def on_mbSalir_activate(self, widget):
        """
        Gestiona el apartado "Salir" del menubar.
        Cierra la aplicación preguntando antes al usuario.
            :param widget: Contiene el widget del menubutton.
            :return: No retorna nada.

        """
        variables.vensalir.connect('delete-event', lambda w, e: w.hide() or True)
        variables.vensalir.show()

    def on_mbAcercade_activate(self, widget):
        """
        Gestiona el apartado "Acerca De" del menubar.
        Abre una ventana con información del hotel, de la aplicación y un enlace a la documentación.
            :param widget: Contiene el widget del menubutton.
            :return: No retorna nada.

        """
        variables.venacercade.connect('delete-event', lambda w, e: w.hide() or True)
        variables.venacercade.show()

    def on_mbBackup_activate(self, widget):
        """
        Gestiona el apartado "Backup" del menubar.
        Crea un backup del estado actual de la base de datos en la carpeta "Backups"
        dentro del directorio de la aplicación.
            :param widget: Contiene el widget del menubutton.
            :return: No retorna nada.

        """
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
        """
        Gestiona el apartado "Importar" del menubar.
        Importa un fichero excel que contenga datos de clientes a la aplicación.
            :param widget: Contiene el widget del menubutton.
            :return: No retorna nada.

        """
        document = xlrd.open_workbook("./datos/listadoclientes.xlsx")
        clientes = document.sheet_by_index(0)
        # Leemos el número de filas y columnas de la hoja de clientes
        filas_clientes = clientes.nrows
        columnas_clientes = clientes.ncols
        for i in range(1, clientes.nrows):
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
        """
        Gestiona el apartado "Exportar" del menubar.
        Exporta los datos de los clientes a un fichero '.xls'.
            :param widget: Contiene el widget del menubutton.
            :return: No retorna nada.

        """
        # Definicion de estilos
        style0 = xlwt.easyxf("font: name Times New Roman, colour red, bold on")
        # style1 = xlwt.easyxf("num_format_str='DD-MMM-YY'")
        style1 = XFStyle()
        style1.num_format_str = 'DD-MMM-YY'
        # Creamos el fichero excel
        wb = xlwt.Workbook()
        # le añadimos una hoja llamada NuevoClientes que permite sobreescribir celdas
        ws = wb.add_sheet("NuevoClientes", cell_overwrite_ok=True)
        ws.write(0, 0, "DNI", style0)
        ws.write(0, 1, "APELIDOS", style0)
        ws.write(0, 2, "NOMBRE", style0)
        ws.write(0, 3, "FECHA ALTA", style0)
        # Aquí consultamos un listado de clientes de la base de datos
        listado = funcionescli.listar()
        # Aqui recorremos el listado e insertamos en la celda correspondiente
        for registro in listado:
            i = listado.index(registro)
            for dato in registro:
                j = registro.index(dato)
                ws.write(i, j, dato, style1)
        # Guardamos la hoja de cálculo
        wb.save("./datos/ejemplo.xls")
        variables.infocli.set_text("Exportación realizada correctamente")

    def on_mbAbrir_activate(self, widget):
        """
        Gestiona el apartado "Abrir" del menubar.
        Carga una copia de seguridad seleccionada a traves de la ventana de selección de fichero.
            :param widget: Contiene el widget del menubutton.
            :return: No retorna nada.

        """
        variables.venfile.connect('delete-event', lambda w, e: w.hide() or True)
        variables.venfile.show()

    def on_mbPrecios_activate(self, widget):
        """
        Gestiona el apartado "Precios" del menubar.
        Abre la ventana de gestión de precios de los servicios básicos.
            :param widget: Contiene el widget del menubutton.
            :return: No retorna nada.

        """
        variables.venprecios.connect('delete-event', lambda w, e: w.hide() or True)
        variables.venprecios.show()
        funcionesser.listar_precios()

    # Eventos Gestión Precios

    def on_btnGuardarPrecio_clicked(self, widget):
        """
        Gestiona el botón "Guardar" de la ventana de precios.
        Recoge los nuevos precios de los entries y los modifica en la base de datos.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        funcionesser.guardar_precio(variables.precios)
        variables.precios[0].set_text("")
        variables.precios[1].set_text("")
        variables.precios[2].set_text("")

    def on_btnCerrarPrecio_clicked(self, widget):
        """
        Gestiona el botón "Cerrar" de la ventana de precios.
        Cierra la ventana de precios.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        variables.venprecios.hide()

    # Eventos impresion

    def on_btnImprimi_clicked(self, widget):
        """
        Gestiona el botón de imprimir en el campo de la factura.
        Muestra la factura en formato '.pdf'.
            :param widget: Contiene el widget del botón.
            :return: No retorna nada.

        """
        try:
            impresion.factura(variables.datosfactura)
        except:
            print("Error en módulo impresión")
