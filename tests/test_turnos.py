import unittest
from datetime import datetime
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.turno import Turno
from src.exceptions.error import (
    DatoInvalidoException
)

class TestTurno(unittest.TestCase):
    
    def setUp(self):

        self.paciente = Paciente("Ana López", "87654321", "20/05/1990")
        self.medico = Medico("Dr. Pedro Martín", "MP456")
        self.fecha_hora = datetime(2025, 6, 20, 10, 30)
    
    def test_crear_turno_valido(self):

        turno = Turno(self.paciente, self.medico, self.fecha_hora, "Cardiología")
        self.assertEqual(turno.obtener_paciente(), self.paciente)
        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha_hora)
        self.assertEqual(turno.obtener_especialidad(), "Cardiología")
    
    def test_crear_turno_paciente_invalido(self):

        with self.assertRaises(DatoInvalidoException):
            Turno(Paciente("","",""), self.medico, self.fecha_hora, "Cardiología")
    
    def test_crear_turno_medico_invalido(self):

        with self.assertRaises(DatoInvalidoException):
            Turno(self.paciente, Medico("",""), self.fecha_hora, "Cardiología")
    
    def test_crear_turno_especialidad_vacia(self):
        
        with self.assertRaises(DatoInvalidoException):
            Turno(self.paciente, self.medico, self.fecha_hora, "")
            
if __name__ == '__main__':
    unittest.main(verbosity=2)