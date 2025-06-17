import unittest
from src.models.medico import Medico
from src.models.especialidad import Especialidad
from src.exceptions.error import (
    DatoInvalidoException,
    EspecialidadInvalidaException
)

class TestMedico(unittest.TestCase):
    
    def test_crear_medico_valido(self):

        medico = Medico("Dr. Juan García", "MP123")
        self.assertEqual(medico.obtener_matricula(), "MP123")
        self.assertIn("Dr. Juan García", str(medico))
    
    def test_crear_medico_nombre_vacio(self):

        with self.assertRaises(DatoInvalidoException):
            Medico("", "MP123")
    
    def test_crear_medico_matricula_vacia(self):

        with self.assertRaises(DatoInvalidoException):
            Medico("Dr. Juan García", "")
    
    def test_agregar_especialidad_valida(self):

        medico = Medico("Dr. Juan García", "MP123")
        especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad)
        self.assertEqual(len(medico.obtener_especialidades()), 1)
    
    def test_agregar_especialidad_duplicada(self):

        medico = Medico("Dr. Juan García", "MP123")
        especialidad1 = Especialidad("Cardiología", ["lunes"])
        especialidad2 = Especialidad("cardiología", ["martes"])  
        medico.agregar_especialidad(especialidad1)
        with self.assertRaises(EspecialidadInvalidaException):
            medico.agregar_especialidad(especialidad2)
    
    def test_obtener_especialidad_para_dia(self):

        medico = Medico("Dr. Juan García", "MP123")
        especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad)
        
        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Cardiología")
        self.assertIsNone(medico.obtener_especialidad_para_dia("martes"))

if __name__ == '__main__':
    unittest.main(verbosity=2)