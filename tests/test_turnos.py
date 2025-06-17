import unittest
from datetime import datetime
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.turno import Turno
from src.models.especialidad import Especialidad
from src.models.clinica import Clinica
from src.exceptions.error import (
    DatoInvalidoException,
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException
)

class TestTurno(unittest.TestCase):
    
    def setUp(self):
        self.clinica = Clinica()

        # Crear pacientes de prueba
        self.paciente1 = Paciente("Lucia Herrera", "99887766", "05/01/1988")
        self.paciente2 = Paciente("Martin Diaz", "66554433", "18/09/1992")
        
        # Crear medicos de prueba
        self.medico1 = Medico("Dr. Alejandro Ruiz", "MP201")
        self.medico2 = Medico("Dra. Sofia Castro", "MP202")
        
        # Crear especialidades (sin tilde en miércoles para que coincida con la normalización)
        self.especialidad_cardiologia = Especialidad("Cardiologia", ["lunes", "miercoles", "viernes"])
        self.especialidad_pediatria = Especialidad("Pediatria", ["martes", "jueves"])

        # Pacientes y médicos adicionales para tests específicos
        self.paciente = Paciente("Ana López", "87654321", "20/05/1990")
        self.medico = Medico("Dr. Pedro Martín", "MP456")
        self.fecha_hora = datetime(2025, 6, 20, 10, 30)
    
    #Turno valido

    def test_crear_turno_valido(self):

        turno = Turno(self.paciente, self.medico, self.fecha_hora, "Cardiología")
        self.assertEqual(turno.obtener_paciente(), self.paciente)
        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha_hora)
        self.assertEqual(turno.obtener_especialidad(), "Cardiología")
    
    def test_agendar_turno_valido(self):

        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_lunes = datetime(2025, 6, 23, 10, 0)
        self.clinica.agendar_turno("99887766", "MP201", "Cardiologia", fecha_lunes)
        
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].obtener_especialidad(), "Cardiologia")
        self.assertEqual(turnos[0].obtener_paciente().obtener_dni(), "99887766")
        self.assertEqual(turnos[0].obtener_medico().obtener_matricula(), "MP201")
    
    def test_multiples_especialidades_mismo_medico(self):

        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.medico1.agregar_especialidad(self.especialidad_pediatria)
        
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_lunes = datetime(2025, 6, 23, 10, 0)
        self.clinica.agendar_turno("99887766", "MP201", "Cardiologia", fecha_lunes)
        
        fecha_martes = datetime(2025, 6, 24, 11, 0)
        self.clinica.agendar_turno("66554433", "MP201", "Pediatria", fecha_martes)
        
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 2)
        
        especialidades_agendadas = [turno.obtener_especialidad() for turno in turnos]
        self.assertIn("Cardiologia", especialidades_agendadas)
        self.assertIn("Pediatria", especialidades_agendadas)
    
    #No existen o disponible

    def test_agendar_turno_paciente_inexistente(self):

        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_medico(self.medico1)
        
        fecha = datetime(2025, 6, 23, 10, 0)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "MP201", "Cardiologia", fecha)
    
    def test_agendar_turno_medico_inexistente(self):

        self.clinica.agregar_paciente(self.paciente1)
        
        fecha = datetime(2025, 6, 23, 10, 0)
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agendar_turno("99887766", "MP999", "Cardiologia", fecha)
    
    def test_agendar_turno_medico_no_atiende_especialidad(self):
        
        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_martes = datetime(2025, 6, 24, 10, 0) 
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("99887766", "MP201", "Pediatria", fecha_martes)
    
    def test_agendar_turno_medico_no_atiende_dia(self):

        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_martes = datetime(2025, 6, 24, 10, 0)  
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("99887766", "MP201", "Cardiologia", fecha_martes)
    
    #Campos invalidos

    def test_crear_turno_especialidad_vacia(self):

        with self.assertRaises(DatoInvalidoException):
            Turno(self.paciente, self.medico, self.fecha_hora, "")
    
    def test_crear_turno_especialidad_solo_espacios(self):
        
        with self.assertRaises(DatoInvalidoException):
            Turno(self.paciente, self.medico, self.fecha_hora, "   ")

    def test_crear_turno_fecha_pasada(self):

        fecha_pasada = datetime(2020, 1, 1, 10, 0)
        with self.assertRaises(DatoInvalidoException):
            Turno(self.paciente, self.medico, fecha_pasada, "Cardiología")
    
    #Turno duplicado

    def test_agendar_turno_duplicado(self):

        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)
        
        fecha = datetime(2025, 6, 23, 10, 0)  

        self.clinica.agendar_turno("99887766", "MP201", "Cardiologia", fecha)
        
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("66554433", "MP201", "Cardiologia", fecha)
    
if __name__ == '__main__':
    unittest.main(verbosity=2)