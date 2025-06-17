import unittest
from datetime import datetime
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.receta import Receta
from src.exceptions.error import (
    RecetaInvalidaException,
    DatoInvalidoException
)

class TestReceta(unittest.TestCase):
    
    def setUp(self):

        self.paciente = Paciente("María González", "11223344", "10/08/1975")
        self.medico = Medico("Dra. Laura Fernández", "MP789")
    
    def test_crear_receta_valida(self):

        medicamentos = ["Aspirina 100mg", "Enalapril 10mg"]
        receta = Receta(self.paciente, self.medico, medicamentos)
        self.assertEqual(receta.obtener_paciente(), self.paciente)
        self.assertEqual(receta.obtener_medico(), self.medico)
        self.assertIsInstance(receta.obtener_fecha(), datetime)
    
    def test_crear_receta_sin_medicamentos(self):

        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, [])
    
    def test_crear_receta_medicamentos_vacios(self):

        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, ["", "  "])
    
    def test_crear_receta_paciente_invalido(self):

        with self.assertRaises(DatoInvalidoException):
            Receta(Paciente("","",""), self.medico, ["Aspirina"])

if __name__ == '__main__':
    unittest.main(verbosity=2)