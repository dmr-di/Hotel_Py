from unittest import TestCase


class Test(TestCase):
    def test_comprobar_dni(self):
        from funcionescli import comprobarDni
        self.assertTrue(comprobarDni("53819899A"))
