from unittest import TestCase


class Test(TestCase):
    def test_comprobardisponibilidad(self):
        from funcionesres import comprobardisponibilidad
        import conexion
        conexion.Conexion().abrirbbdd()
        self.assertTrue(comprobardisponibilidad(105))
        conexion.Conexion.cerrarbbdd(self)
