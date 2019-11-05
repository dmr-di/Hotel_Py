import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import conexion, variables, funcionescli, funcioneshab

class Eventos():

    #Eventos generales

    def on_venPrincipal_destroy(self, widget):
        conexion.Conexion().cerrarbbdd()
        Gtk.main_quit()

    def on_btnSalir_clicked(self, widget):
        conexion.Conexion().cerrarbbdd()
        Gtk.main_quit()

    def on_btnSalirhab_clicked(self, widget):
        conexion.Conexion().cerrarbbdd()
        Gtk.main_quit()


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
            print('error en boton modificar')

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
        except:
            print("Error cargar cliente")

    def on_btnCalendar_clicked(self, widget):
        try:
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print("Error abrir calendario")

    def on_Calendar_day_selected_double_click(self, widget):
        try:
            agno, mes, dia = variables.calendar.get_date()
            fecha = "%s/"%dia+"%s/"%(mes+1)+"%s"%agno
            variables.filacli[3].set_text(fecha)
            variables.vencalendar.hide()
        except:
            print('Error al coger la fecha')

    #Eventos Habitaciones

    def on_btnAltahab_clicked(self, widget):
        try:
            numero = variables.filahab[0].get_text()
            tipo = funcioneshab.seleccionRB()
            precio = variables.filahab[1].get_text()
            precio = float(precio)
            precio = round(precio, 2)
            registro = (numero, tipo, precio)
            if numero != '' and tipo != '':
                funcioneshab.insertarhab(registro)
                funcioneshab.listadohab(variables.listhabitaciones)
                funcioneshab.limpiarEntry(variables.filahab)
                variables.infohab.set_text("Alta realizada correctamente")
        except:
            print('Error alta habitacion')