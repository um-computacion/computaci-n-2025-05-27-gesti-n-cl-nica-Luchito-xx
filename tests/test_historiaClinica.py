import unittest
from datetime import datetime
from src.models.paciente import Paciente
from src.models.historiaClinica import HistoriaClinica
from src.models.medico import Medico
from src.models.turno import Turno
from src.models.receta import Receta
from src.exceptions.error import (
    DatoInvalidoException
)

class TestHistoriaClinica(unittest.TestCase):
    
    def setUp(self):

        self.paciente = Paciente("Carlos Rodríguez", "55667788", "25/12/1980")
        self.medico = Medico("Dr. Roberto Silva", "MP101")
        self.historia = HistoriaClinica(self.paciente)
    
    def test_crear_historia_clinica_valida(self):

        self.assertEqual(len(self.historia.obtener_turnos()), 0)
        self.assertEqual(len(self.historia.obtener_recetas()), 0)
    
    def test_agregar_turno_a_historia(self):

        turno = Turno(self.paciente, self.medico, datetime(2025, 6, 20, 15, 0), "Medicina General")
        self.historia.agregar_turno(turno)
        self.assertEqual(len(self.historia.obtener_turnos()), 1)
    
    def test_agregar_receta_a_historia(self):

        receta = Receta(self.paciente, self.medico, ["Paracetamol"])
        self.historia.agregar_receta(receta)
        self.assertEqual(len(self.historia.obtener_recetas()), 1)
    
    def test_crear_historia_paciente_invalido(self):

        with self.assertRaises(DatoInvalidoException):
            HistoriaClinica(Paciente("","",""))
            
if __name__ == '__main__':
    unittest.main(verbosity=2)