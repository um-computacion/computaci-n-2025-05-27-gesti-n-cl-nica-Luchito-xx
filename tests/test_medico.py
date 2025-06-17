import unittest
from src.models.medico import Medico
from src.models.clinica import Clinica
from src.exceptions.error import (
    DatoInvalidoException,
    MedicoDuplicadoException,
    MedicoNoEncontradoException
)

class TestMedico(unittest.TestCase):
 
    def setUp(self):

        self.clinica = Clinica()
        
        # Crear medicos de prueba
        self.medico1 = Medico("Dr. Alejandro Ruiz", "MP201")
        self.medico2 = Medico("Dra. Sofia Castro", "MP202")

    #Crear medico valido
    def test_agregar_medico_valido(self):

        self.clinica.agregar_medico(self.medico1)
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0].obtener_matricula(), "MP201")
        
    #Medico duplicado
    def test_agregar_medico_duplicado(self):

        medico = Medico("Dr. Juan García", "MP123")
        self.assertEqual(medico.obtener_matricula(), "MP123")
        self.assertIn("Dr. Juan García", str(medico))


        medico_duplicado = Medico("Otro Doctor", "MP201")
        with self.assertRaises(MedicoDuplicadoException):
            self.clinica.agregar_medico(medico_duplicado)
    
    #Obtener medico
    def test_obtener_medico_por_matricula_existente(self):

        self.clinica.agregar_medico(self.medico1)
        medico_obtenido = self.clinica.obtener_medico_por_matricula("MP201")
        self.assertEqual(medico_obtenido, self.medico1)
    
    def test_obtener_medico_por_matricula_inexistente(self):

        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.obtener_medico_por_matricula("MP999")
    
    #Campos invalidos
    def test_crear_medico_nombre_vacio(self):

        with self.assertRaises(DatoInvalidoException):
            Medico("", "MP123")
    
    def test_crear_medico_matricula_vacia(self):

        with self.assertRaises(DatoInvalidoException):
            Medico("Dr. Juan García", "")
    

if __name__ == '__main__':
    unittest.main(verbosity=2)