import unittest

import main
class TestearFormato(unittest.TestCase):
    def setUp(self):
        self.formato=Descifrador("mensaje_marciano.txt")
    #este test debería estar ok
    def test_archivo(self):
    	self.assertEqual(type(formato.texto),type("string"))   
        self.assertEqual(len(formato.texto)==253)
    	self.assertEqual(sum(map(formato.text)==253))

class TestearMensaje(unittest.TestCase):
    def setUp(self):
        self.formato=Descifrador("mensaje_marciano.txt")
        self.mensaeje=CustomExpection("mensaje_marciano.txt")
    #este test debería estar ok
    def test_incorrectos(self):
    	self.IsNotNone(CustomExpection.lista)
   
    def test_caracteres(self):
    	self.IsNotNone(CustomExpection.caracteres)

    def test_codificacion(self):
    	self.In(0,formato.texto)
    	self.In(1,formato.texto)

def main():
	Tsuite = unittest.TestSuite()
	Tsuite = addTest(unittest.TestLoader().loadTestsFromTestCase(TestearFormato))
	Tsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestearMensaje))
	return unittest.TextTestRunner().run(Tsuite)
if __name__ == '__main__':
    main()
