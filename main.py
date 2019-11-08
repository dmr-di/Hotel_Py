import funcioneshab

__autor__='danimr'

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import eventos, conexion, variables, funcionescli

'''
El main contiene los elementos necesarios para lanzar la aplicación
asi como la declaración de los widgets que se usarán. También los
módulos que tenemos que importar de las librerias gráficas
'''

class Empresa:
    def __init__(self):
        #iniciamos la libreria Gtk
        self.b = Gtk.Builder()
        self.b.add_from_file('ventana.glade')
        #cargamos los widgets con evento asociado
        self.vprincipal = self.b.get_object('venPrincipal')
        self.vencalendar = self.b.get_object('venCalendar')
        self.calendar = self.b.get_object('Calendar')
        variables.panel = self.b.get_object('Panel')

        #declaración de widgets
        self.entdni = self.b.get_object('entDni')
        self.entapel = self.b.get_object('entApel')
        self.entnome = self.b.get_object('entNome')
        self.entdatacli = self.b.get_object('entDatacli')
        self.lblmensajedni = self.b.get_object('lblMensajeDNI')
        self.entnumero = self.b.get_object('entNumhab')
        self.entprecio = self.b.get_object('entPrecio')
        self.calendar = self.b.get_object('Calendar')
        self.rbsimple = self.b.get_object('rbSimple')
        self.rbdoble = self.b.get_object('rbDoble')
        self.rbfamiliar = self.b.get_object('rbFamiliar')
        variables.filacli = (self.entdni, self.entapel, self.entnome, self.entdatacli)
        variables.listclientes = self.b.get_object('listClientes')
        variables.treeclientes = self.b.get_object('treeClientes')
        variables.filahab = (self.entnumero, self.entprecio)
        variables.listhabitaciones = self.b.get_object('listHabitaciones')
        variables.treehabitaciones = self.b.get_object('treeHabitaciones')
        variables.rbgrouphab = (self.rbsimple, self.rbdoble, self.rbfamiliar)
        variables.lblcodigo = self.b.get_object('lblCodcli')
        variables.mensajerr = self.lblmensajedni
        variables.infocli = self.b.get_object('lblInfocli')
        variables.infohab = self.b.get_object('lblInfohab')
        variables.fecha = self.b.get_object('lblFecha')
        variables.vencalendar = self.vencalendar
        variables.calendar = self.calendar

        #conectamos y mostramos
        self.b.connect_signals(eventos.Eventos())
        self.vprincipal.show()
        conexion.Conexion().abrirbbdd()
        funcionescli.listadocli(variables.listclientes)
        funcioneshab.listadohab(variables.listhabitaciones)

if __name__=='__main__':
    main = Empresa()
    Gtk.main()