import unittest
from src.models.paciente import Paciente
from src.exceptions.error import DatoInvalidoException

class TestPaciente(unittest.TestCase):
    
    def test_crear_paciente_valido(self): 

        paciente = Paciente("Juan Pérez", "12345678", "15/03/1985")
        self.assertEqual(paciente.obtener_dni(), "12345678")
        self.assertIn("Juan Pérez", str(paciente))
    
    def test_crear_paciente_nombre_vacio(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("", "12345678", "15/03/1985")
    
    def test_crear_paciente_dni_vacio(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan Pérez", "", "15/03/1985")
    
    def test_crear_paciente_fecha_vacia(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan Pérez", "12345678", "")


if __name__ == '__main__':
    unittest.main(verbosity=2)