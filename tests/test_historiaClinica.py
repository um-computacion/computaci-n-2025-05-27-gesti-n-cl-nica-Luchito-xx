import unittest
from datetime import datetime
from src.models.paciente import Paciente
from src.models.historiaClinica import HistoriaClinica
from src.models.medico import Medico
from src.models.turno import Turno
from src.models.receta import Receta
from src.models.clinica import Clinica

class TestHistoriaClinica(unittest.TestCase):
    
    def setUp(self):
        self.clinica = Clinica()
        
        self.paciente = Paciente("Carlos Rodríguez", "55667788", "25/12/1980")
        self.medico = Medico("Dr. Roberto Silva", "MP101")
        
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        
        self.historia = HistoriaClinica(self.paciente)
    
    # Creación válida
    
    def test_crear_historia_clinica_valida(self):

        self.assertEqual(len(self.historia.obtener_turnos()), 0)
        self.assertEqual(len(self.historia.obtener_recetas()), 0)
    
    def test_agregar_turno_a_historia(self):

        turno = Turno(self.paciente, self.medico, datetime(2025, 6, 20, 15, 0), "Medicina General")
        self.historia.agregar_turno(turno)
        self.assertEqual(len(self.historia.obtener_turnos()), 1)
        
        turnos = self.historia.obtener_turnos()
        self.assertEqual(turnos[0].obtener_paciente().obtener_dni(), "55667788")
        self.assertEqual(turnos[0].obtener_especialidad(), "Medicina General")

    def test_agregar_receta_a_historia(self):

        receta = Receta(self.paciente, self.medico, ["Paracetamol"])
        self.historia.agregar_receta(receta)
        self.assertEqual(len(self.historia.obtener_recetas()), 1)
        
        recetas = self.historia.obtener_recetas()
        self.assertEqual(recetas[0].obtener_paciente().obtener_dni(), "55667788")

    # Guardado de turnos y recetas 

    def test_historia_clinica_contiene_turnos_y_recetas_via_clinica(self):

        self.clinica.emitir_receta("55667788", "MP101", ["Aspirina"])

        historia = self.clinica.obtener_historia_clinica("55667788")
        
        self.assertEqual(len(historia.obtener_recetas()), 1)
        
        recetas = historia.obtener_recetas()
        self.assertEqual(recetas[0].obtener_paciente().obtener_dni(), "55667788")
        self.assertEqual(recetas[0].obtener_medico().obtener_matricula(), "MP101")
    
    def test_historia_clinica_multiples_registros(self):

        turno1 = Turno(self.paciente, self.medico, datetime(2025, 6, 20, 15, 0), "Medicina General")
        turno2 = Turno(self.paciente, self.medico, datetime(2025, 6, 25, 10, 0), "Cardiología")
        self.historia.agregar_turno(turno1)
        self.historia.agregar_turno(turno2)
        
        self.clinica.emitir_receta("55667788", "MP101", ["Aspirina", "Paracetamol"])
        self.clinica.emitir_receta("55667788", "MP101", ["Ibuprofeno"])
        
        historia = self.clinica.obtener_historia_clinica("55667788")
        
        self.assertEqual(len(historia.obtener_turnos()), 2)
        self.assertEqual(len(historia.obtener_recetas()), 2)
    
    #Obtner turnos y recetas

    def test_obtener_turnos_devuelve_copia(self):

        turno = Turno(self.paciente, self.medico, datetime(2025, 6, 20, 15, 0), "Medicina General")
        self.historia.agregar_turno(turno)
        
        turnos = self.historia.obtener_turnos()
        turnos.clear() 

        self.assertEqual(len(self.historia.obtener_turnos()), 1)
    
    def test_obtener_recetas_devuelve_copia(self):

        receta = Receta(self.paciente, self.medico, ["Paracetamol"])
        self.historia.agregar_receta(receta)
        
        recetas = self.historia.obtener_recetas()
        recetas.clear()  

        self.assertEqual(len(self.historia.obtener_recetas()), 1)
            
if __name__ == '__main__':
    unittest.main(verbosity=2)