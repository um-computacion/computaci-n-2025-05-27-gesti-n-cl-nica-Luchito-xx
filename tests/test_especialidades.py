import unittest
from src.models.clinica import Clinica
from src.models.medico import Medico
from src.models.especialidad import Especialidad
from src.exceptions.error import (
    DatoInvalidoException,
    MedicoNoEncontradoException,
    EspecialidadInvalidaException
)

class TestEspecialidad(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()

        self.medico = Medico("Dr. Juan Pérez", "MP123")
        self.clinica.agregar_medico(self.medico)
    
    #Creacion valida

    def test_crear_especialidad_valida(self):
        especialidad = Especialidad("Cardiología", ["lunes", "miércoles", "viernes"])
        self.assertEqual(especialidad.obtener_especialidad(), "Cardiología")
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertFalse(especialidad.verificar_dia("martes"))

    def test_especialidad_con_tildes_normalizada(self):
        especialidad = Especialidad("Cardiología", ["miércoles"])  

        self.assertTrue(especialidad.verificar_dia("miércoles"))
        self.assertTrue(especialidad.verificar_dia("miercoles"))  
        self.assertTrue(especialidad.verificar_dia("MIÉRCOLES"))  
    
    #Campos invalidos
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
    
    #Agregado de especialidad a medico
    def test_agregar_especialidad_a_medico_registrado(self):
        especialidad = Especialidad("Cardiología", ["lunes", "martes"])
        
        self.assertEqual(len(self.medico.obtener_especialidades()), 0)
    
        self.medico.agregar_especialidad(especialidad)
    
        especialidades = self.medico.obtener_especialidades()
        self.assertEqual(len(especialidades), 1)
        self.assertEqual(especialidades[0].obtener_especialidad(), "Cardiología")
        
        self.assertEqual(self.medico.obtener_especialidad_para_dia("lunes"), "Cardiología")
        self.assertIsNone(self.medico.obtener_especialidad_para_dia("miércoles"))

    def test_multiples_especialidades_mismo_medico(self):
        cardiologia = Especialidad("Cardiología", ["lunes", "martes"])
        neurologia = Especialidad("Neurología", ["miércoles", "jueves"])
        
        self.medico.agregar_especialidad(cardiologia)
        self.medico.agregar_especialidad(neurologia)
        
        especialidades = self.medico.obtener_especialidades()
        self.assertEqual(len(especialidades), 2)
        
        self.assertEqual(self.medico.obtener_especialidad_para_dia("lunes"), "Cardiología")
        self.assertEqual(self.medico.obtener_especialidad_para_dia("miércoles"), "Neurología")
        self.assertIsNone(self.medico.obtener_especialidad_para_dia("viernes"))
    
    #Especilidad duplicada medico
    def test_evitar_duplicados_especialidad_mismo_medico(self):
        especialidad1 = Especialidad("Cardiología", ["lunes", "martes"])
        especialidad2 = Especialidad("Cardiología", ["miércoles", "jueves"])  

        self.medico.agregar_especialidad(especialidad1)
        
        with self.assertRaises(EspecialidadInvalidaException) as context:
            self.medico.agregar_especialidad(especialidad2)
        
        self.assertIn("ya tiene la especialidad", str(context.exception))
        
        self.assertEqual(len(self.medico.obtener_especialidades()), 1)
    
    def test_evitar_duplicados_case_insensitive(self):
        especialidad1 = Especialidad("Cardiología", ["lunes"])
        especialidad2 = Especialidad("CARDIOLOGÍA", ["martes"])  

        self.medico.agregar_especialidad(especialidad1)
        
        with self.assertRaises(EspecialidadInvalidaException):
            self.medico.agregar_especialidad(especialidad2)
    
    #Agregado de especialidad a medico no registrado

    def test_agregar_especialidad_a_medico_no_registrado(self):

        medico_no_registrado = Medico("Dr. No Registrado", "MP999")
        especialidad = Especialidad("Medicina General", ["lunes", "martes"])
        
        medico_no_registrado.agregar_especialidad(especialidad)
        self.assertEqual(len(medico_no_registrado.obtener_especialidades()), 1)
        
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.obtener_medico_por_matricula("MP999")

if __name__ == '__main__':
    unittest.main(verbosity=2)