from datos import filtrar, evaluar, PROM, MEDIAN, VAR, DESV, comparar_columna, do_if
import unittest


class TestearEstadisticas(unittest.TestCase):

    def setUp(self):
        self.stats = [1, 2, 3, 4, 5, 6]

    def test_median(self):
        self.assertRaises(Exception, MEDIAN, "S")
        self.assertEqual(MEDIAN(self.stats), 3.5)

    def test_median(self):
        with self.assertRaises(Exception):
            MEDIAN("S")

    def test_prom(self):
        self.assertEqual(PROM(self.stats), 3.5)
        self.assertRaises(ZeroDivisionError, PROM, [])
        self.assertRaises(Exception, MEDIAN, "S")

    def test_prom_error(self):
        with self.assertRaises(ZeroDivisionError):
            PROM([])
        with self.assertRaises(Exception):
            PROM(())

    def test_fitrar(self):
        self.assertEqual(filtrar(self.stats, ">", 3), [4, 5, 6])
        self.assertEqual(filtrar(self.stats, "==", 3), [3])

    def test_var(self):
        self.assertEqual(round(VAR([5, 1, 1, 5]), 1), 7.1)
        self.assertRaises(Exception, VAR, "string")
        self.assertRaises(ZeroDivisionError, VAR, [0.999])

    def test_var_error(self):
        with self.assertRaises(Exception):
            VAR("string")
        with self.assertRaises(ZeroDivisionError):
            VAR([0.999])

    def test_desv(self):
        self.assertRaises(Exception, DESV, "string")
        self.assertRaises(ZeroDivisionError, DESV, [0.689])

    def test_desv_error(self):

        with self.assertRaises(Exception):
            DESV("string")
        with self.assertRaises(ZeroDivisionError):
            DESV([0.689])

    def test_compara_col(self):
        self.assertEqual(comparar_columna(
            [2131.2, 52.2, 2311.1, 2321.1], ">", "PROM", self.stats), True)
        self.assertRaises(Exception, comparar_columna,
                          "deberia_ser_lista", "<", "PROM", self.stats)

    def test_compara_col_error(self):
        with self.assertRaises(Exception):
            comparar_columna("deberia_ser_lista", "<", "PROM", self.stats)
   

    def test_do_if(self):
        pass

    def test_do_if_error(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestearEstadisticas)
unittest.TextTestRunner().run(suite)
