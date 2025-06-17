import unittest
from src.models.paciente import Paciente
from src.models.clinica import Clinica
from src.models.historiaClinica import HistoriaClinica
from src.exceptions.error import (
    DatoInvalidoException
)

class TestPaciente(unittest.TestCase):

    def setUp(self):

        self.clinica = Clinica()
            
        self.paciente = Paciente("Lucia Herrera", "99887766", "05/01/1988")

    #Paciente duplicado
    
    def test_agregar_paciente_duplicado(self):

        self.clinica.agregar_paciente(self.paciente)
        paciente_duplicado = Paciente("Otro Nombre", "99887766", "01/01/2000")
        with self.assertRaises(DatoInvalidoException):
            self.clinica.agregar_paciente(paciente_duplicado)

    #Creacion valida

    def test_crear_paciente_valido(self): 

        self.clinica.agregar_paciente(self.paciente)
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0].obtener_dni(), "99887766")

        # Verificar que se creo la historia clinica
        historia = self.clinica.obtener_historia_clinica("99887766")
        self.assertIsInstance(historia, HistoriaClinica)

    #Campos invalidos

    def test_crear_paciente_nombre_vacio(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("", "12345678", "15/03/1985")
    
    def test_crear_paciente_dni_vacio(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan Pérez", "", "15/03/1985")
    
    def test_crear_paciente_fecha_vacia(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan Pérez", "12345678", "")

    def test_crear_paciente_fecha_formato_invalido(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan Pérez", "12345678", "00-01-2001")

    def test_crear_paciente_dni_con_letras(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan Pérez", "1234567a", "15/03/1985")
    
    def test_crear_paciente_dni_largo_incorrecto(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan Pérez", "123456789", "15/03/1985")
        
        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan Pérez", "1234567", "15/03/1985")
    
    def test_crear_paciente_nombre_con_numeros(self):

        with self.assertRaises(DatoInvalidoException):
            Paciente("Juan123", "12345678", "15/03/1985")
    
    def test_crear_paciente_nombre_muy_largo(self):

        nombre_largo = "A" * 51
        with self.assertRaises(DatoInvalidoException):
            Paciente(nombre_largo, "12345678", "15/03/1985")


if __name__ == '__main__':
    unittest.main(verbosity=2)