__autor__='danimr'

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, Gdk

import eventos, conexion, variables, funcionescli, funcioneshab, funcionesres

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
        self.venacercade = self.b.get_object('venAcercade')
        self.venfile = self.b.get_object('venFiledialog')
        self.calendar = self.b.get_object('Calendar')
        self.vprecios = self.b.get_object('venPrecios')
        variables.panel = self.b.get_object('Panel')
        self.estilopanel = variables.panel.get_style_context()
        self.menubar = self.b.get_object('MenuBar').get_style_context()

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
        self.entchkin = self.b.get_object('entChkin')
        self.entchkout = self.b.get_object('entChkout')
        self.numfac = self.b.get_object('lblSNumFac')
        self.lbldnifac = self.b.get_object('lblSDniFac')
        self.lblapelfac = self.b.get_object('lblSApelFac')
        self.lblnomeclifac = self.b.get_object('lblSNomecliFac')
        self.lblnumhabfac = self.b.get_object('lblSNumhabFac')
        self.lbltipohabfac = self.b.get_object('lblSTipohabFac')
        self.lbldatafac = self.b.get_object('lblSDataFac')
        self.lblconcepto1 = self.b.get_object('lblConcepto1')
        self.lblunidades1 = self.b.get_object('lblUnidades1')
        self.lblprecio1 = self.b.get_object('lblPrecio1')
        self.lbltotal1 = self.b.get_object('lblTotal1')
        self.lblconcepto2 = self.b.get_object('lblConcepto2')
        self.lblunidades2 = self.b.get_object('lblUnidades2')
        self.lblprecio2 = self.b.get_object('lblPrecio2')
        self.lbltotal2 = self.b.get_object('lblTotal2')
        self.lblconcepto3 = self.b.get_object('lblConcepto3')
        self.lblunidades3 = self.b.get_object('lblUnidades3')
        self.lblprecio3 = self.b.get_object('lblPrecio3')
        self.lbltotal3 = self.b.get_object('lblTotal3')
        self.lblconcepto4 = self.b.get_object('lblConcepto4')
        self.lblunidades4 = self.b.get_object('lblUnidades4')
        self.lblprecio4 = self.b.get_object('lblPrecio4')
        self.lbltotal4 = self.b.get_object('lblTotal4')
        self.lblconcepto5 = self.b.get_object('lblConcepto5')
        self.lblunidades5 = self.b.get_object('lblUnidades5')
        self.lblprecio5 = self.b.get_object('lblPrecio5')
        self.lbltotal5 = self.b.get_object('lblTotal5')
        self.lblcodresser = self.b.get_object('lblCodResSer')
        self.lblnumhabser = self.b.get_object('lblNHabSer')
        self.rbdesayuno = self.b.get_object('rbDesayuno')
        self.rbcomida = self.b.get_object('rbComida')
        self.rbotro = self.b.get_object('rbOtro')
        self.sptservicios = self.b.get_object('sptServicios')
        self.lblservicios = self.b.get_object('lblServicios')
        self.boxservicios = self.b.get_object('boxServicios')
        self.entdesayuno = self.b.get_object('entPrecioDes')
        self.entcomida = self.b.get_object('entPrecioCom')
        self.entparking = self.b.get_object('entPrecioPar')
        self.entser = self.b.get_object('entTipoSer')
        self.entserprecio = self.b.get_object('entPrecioSer')
        variables.lblfile = self.b.get_object('lblFile')
        variables.filacli = (self.entdni, self.entapel, self.entnome, self.entdatacli)
        variables.listclientes = self.b.get_object('listClientes')
        variables.treeclientes = self.b.get_object('treeClientes')
        variables.filahab = (self.entnumero, self.entprecio)
        variables.listhabitaciones = self.b.get_object('listHabitaciones')
        variables.treehabitaciones = self.b.get_object('treeHabitaciones')
        variables.listservicios = self.b.get_object('listServicios')
        variables.treeservicios = self.b.get_object('treeServicios')
        variables.filares = (self.entchkin, self.entchkout)
        variables.listreshab = self.b.get_object('listReshab')
        variables.listreservas = self.b.get_object('listReservas')
        variables.treereservas = self.b.get_object('treeReservas')
        variables.rbgrouphab = (self.rbsimple, self.rbdoble, self.rbfamiliar)
        variables.lblcodigo = self.b.get_object('lblCodcli')
        variables.mensajerr = self.lblmensajedni
        variables.infocli = self.b.get_object('lblInfocli')
        variables.infohab = self.b.get_object('lblInfohab')
        variables.infores = self.b.get_object('lblInfores')
        variables.fecha = self.b.get_object('lblFecha')
        variables.vencalendar = self.vencalendar
        variables.venacercade = self.venacercade
        variables.venprecios = self.vprecios
        variables.calendar = self.calendar
        variables.venfile = self.venfile
        variables.lbldnires = self.b.get_object('lblDnires')
        variables.lblapelres = self.b.get_object('lblApelres')
        variables.lblnoches = self.b.get_object('lblNoches')
        variables.cbreshab = self.b.get_object('cbReshab')
        variables.switch = self.b.get_object('swLibre')
        variables.cbparking = self.b.get_object('cbParking')
        variables.factura = (self.numfac, self.lbldnifac, self.lblapelfac, self.lblnomeclifac,
                             self.lblnumhabfac, self.lbltipohabfac, self.lbldatafac)
        variables.servicio = (self.lblconcepto1, self.lblunidades1, self.lblprecio1, self.lbltotal1)
        variables.grid_factura = ((self.lblconcepto2, self.lblunidades2, self.lblprecio2, self.lbltotal2),
                                  (self.lblconcepto3, self.lblunidades3, self.lblprecio3, self.lbltotal3),
                                  (self.lblconcepto4, self.lblunidades4, self.lblprecio4, self.lbltotal4),
                                  (self.lblconcepto5, self.lblunidades5, self.lblprecio5, self.lbltotal5))
        variables.datos_servicio = (self.lblcodresser, self.lblnumhabser)
        variables.rgservicios = (self.rbdesayuno, self.rbcomida, self.rbotro)
        variables.servicios_adicionales = (self.sptservicios, self.lblservicios, self.boxservicios)
        variables.precios = (self.entdesayuno, self.entcomida, self.entparking)
        variables.entser_adicionales = (self.entser, self.entserprecio)

        # Aplicamos los estilos
        self.set_styles()
        self.menubar.add_class('MenuBar')
        self.estilopanel.add_class('Panel')

        # Conectamos y mostramos
        self.b.connect_signals(eventos.Eventos())
        self.vprincipal.show()
        conexion.Conexion().abrirbbdd()
        funcionescli.listadocli(variables.listclientes)
        funcioneshab.listadohab(variables.listhabitaciones)
        funcionesres.listadoreshab(variables.listreshab)
        funcionesres.listadores(variables.listreservas)

    def set_styles(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('estilos.css')
        Gtk.StyleContext().add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

if __name__=='__main__':
    main = Empresa()
    Gtk.main()