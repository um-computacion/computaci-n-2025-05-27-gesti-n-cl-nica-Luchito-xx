import unittest
from datetime import datetime
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.receta import Receta
from src.models.clinica import Clinica
from src.exceptions.error import (
    RecetaInvalidaException,
    DatoInvalidoException,
    PacienteNoEncontradoException,
    MedicoNoEncontradoException
)

class TestReceta(unittest.TestCase):
    
    def setUp(self):

        self.clinica = Clinica()

        self.paciente = Paciente("María González", "11223344", "10/08/1975")
        self.medico = Medico("Dra. Laura Fernández", "MP789")
    
    #Receta valida

    def test_crear_receta_valida(self):
        medicamentos = ["Aspirina 100mg", "Enalapril 10mg"]
        receta = Receta(self.paciente, self.medico, medicamentos)
        
        self.assertEqual(receta.obtener_paciente(), self.paciente)
        self.assertEqual(receta.obtener_medico(), self.medico)
        self.assertIsInstance(receta.obtener_fecha(), datetime)
        
        diferencia = datetime.now() - receta.obtener_fecha()
        self.assertLess(diferencia.total_seconds(), 1)  
    
    #No existen

    def test_emitir_receta_paciente_inexistente(self):

        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("99999999", "MP201", ["Aspirina"])
    
    def test_emitir_receta_medico_inexistente(self):

        self.clinica.agregar_paciente(self.paciente)
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.emitir_receta("99887766", "MP999", ["Aspirina"])

    #Campos invalidos

    def test_crear_receta_sin_medicamentos(self):

        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, [])
    
    def test_crear_receta_medicamentos_vacios(self):

        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, ["", "  "])
    
    def test_crear_receta_paciente_invalido(self):

        with self.assertRaises(DatoInvalidoException):
            Receta(Paciente("","",""), self.medico, ["Aspirina"])

    def test_crear_receta_medico_invalido(self):

        with self.assertRaises(DatoInvalidoException):
            Receta(Paciente("","",""), Medico("", ""), ["Aspirina"])

if __name__ == '__main__':
    unittest.main(verbosity=2)