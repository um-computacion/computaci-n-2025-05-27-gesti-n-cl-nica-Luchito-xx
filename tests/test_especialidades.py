import unittest
from src.models.clinica import Clinica
from src.models.especialidad import Especialidad
from src.exceptions.error import (
    DatoInvalidoException,
    MedicoNoEncontradoException
)


class TestEspecialidad(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()
    
    def test_crear_especialidad_valida(self):

        especialidad = Especialidad("Cardiología", ["lunes", "miércoles", "viernes"])
        self.assertEqual(especialidad.obtener_especialidad(), "Cardiología")
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertFalse(especialidad.verificar_dia("martes"))
    
    def test_crear_especialidad_tipo_vacio(self):

        with self.assertRaises(DatoInvalidoException):
            Especialidad("", ["lunes"])
    
    def test_crear_especialidad_sin_dias(self):

        with self.assertRaises(DatoInvalidoException):
            Especialidad("Cardiología", [])
    
    def test_crear_especialidad_dia_invalido(self):

        with self.assertRaises(DatoInvalidoException):
            Especialidad("Cardiología", ["lunes", "dia_inexistente"])
    
    def test_verificar_dia_case_insensitive(self):

        especialidad = Especialidad("Cardiología", ["lunes"])
        self.assertTrue(especialidad.verificar_dia("LUNES"))
        self.assertTrue(especialidad.verificar_dia("Lunes"))
    
    def test_agregar_especialidad_a_medico_no_registrado(self):
        with self.assertRaises(MedicoNoEncontradoException):
            medico = self.clinica.obtener_medico_por_matricula("MP999")
            medico.agregar_especialidad(Especialidad("Medico General", ["lunes", "martes"]))
            
if __name__ == '__main__':
    unittest.main(verbosity=2)