import unittest
from datetime import datetime
from modelo import (
    Clinica, Paciente, Medico, Especialidad, Turno, Receta, HistoriaClinica,
    PacienteNoEncontradoException, MedicoNoEncontradoException,
    MedicoNoDisponibleException, EspecialidadInvalidaException,
    DatoInvalidoException, TurnoOcupadoException, RecetaInvalidaException
)

class TestClinica(unittest.TestCase):
    
    def setUp(self):

        self.clinica = Clinica()
        
        # Crear pacientes de prueba
        self.paciente1 = Paciente("Lucía Herrera", "99887766", "05/01/1988")
        self.paciente2 = Paciente("Martín Díaz", "66554433", "18/09/1992")
        
        # Crear médicos de prueba
        self.medico1 = Medico("Dr. Alejandro Ruiz", "MP201")
        self.medico2 = Medico("Dra. Sofía Castro", "MP202")
        
        # Crear especialidades
        self.especialidad_cardiologia = Especialidad("Cardiología", ["lunes", "miércoles", "viernes"])
        self.especialidad_pediatria = Especialidad("Pediatría", ["martes", "jueves"])
    
    def test_agregar_paciente_valido(self):

        self.clinica.agregar_paciente(self.paciente1)
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0].obtener_dni(), "99887766")
        
        # Verificar que se creó la historia clínica
        historia = self.clinica.obtener_historia_clinica("99887766")
        self.assertIsInstance(historia, HistoriaClinica)
    
    def test_agregar_paciente_duplicado(self):

        self.clinica.agregar_paciente(self.paciente1)
        paciente_duplicado = Paciente("Otro Nombre", "99887766", "01/01/2000")
        with self.assertRaises(DatoInvalidoException):
            self.clinica.agregar_paciente(paciente_duplicado)
    
    def test_agregar_medico_valido(self):

        self.clinica.agregar_medico(self.medico1)
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0].obtener_matricula(), "MP201")
    
    def test_agregar_medico_duplicado(self):

        self.clinica.agregar_medico(self.medico1)
        medico_duplicado = Medico("Otro Doctor", "MP201")
        with self.assertRaises(DatoInvalidoException):
            self.clinica.agregar_medico(medico_duplicado)
    
    def test_obtener_medico_por_matricula_existente(self):

        self.clinica.agregar_medico(self.medico1)
        medico_obtenido = self.clinica.obtener_medico_por_matricula("MP201")
        self.assertEqual(medico_obtenido, self.medico1)
    
    def test_obtener_medico_por_matricula_inexistente(self):

        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.obtener_medico_por_matricula("MP999")
    
    def test_agendar_turno_valido(self):

        # Configurar datos
        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        # Agendar turno para un lunes (día que atiende cardiología)
        fecha_lunes = datetime(2025, 6, 23, 10, 0)  # Lunes
        self.clinica.agendar_turno("99887766", "MP201", "Cardiología", fecha_lunes)
        
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].obtener_especialidad(), "Cardiología")
    
    def test_agendar_turno_paciente_inexistente(self):

        self.clinica.agregar_medico(self.medico1)
        fecha = datetime(2025, 6, 23, 10, 0)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "MP201", "Cardiología", fecha)
    
    def test_agendar_turno_medico_inexistente(self):

        self.clinica.agregar_paciente(self.paciente1)
        fecha = datetime(2025, 6, 23, 10, 0)
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agendar_turno("99887766", "MP999", "Cardiología", fecha)
    
    def test_agendar_turno_medico_no_atiende_especialidad(self):

        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_lunes = datetime(2025, 6, 23, 10, 0)
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("99887766", "MP201", "Pediatría", fecha_lunes)
    
    def test_agendar_turno_medico_no_atiende_dia(self):

        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        # Martes - día que no atiende cardiología
        fecha_martes = datetime(2025, 6, 24, 10, 0)
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("99887766", "MP201", "Cardiología", fecha_martes)
    
    def test_agendar_turno_duplicado(self):

        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)
        
        fecha = datetime(2025, 6, 23, 10, 0)  # Lunes
        
        # Primer turno - exitoso
        self.clinica.agendar_turno("99887766", "MP201", "Cardiología", fecha)
        
        # Segundo turno en la misma fecha/hora - debe fallar
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("66554433", "MP201", "Cardiología", fecha)
    
    def test_emitir_receta_valida(self):

        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        medicamentos = ["Aspirina 100mg", "Enalapril 10mg"]
        self.clinica.emitir_receta("99887766", "MP201", medicamentos)
        
        # Verificar que la receta se agregó a la historia clínica
        historia = self.clinica.obtener_historia_clinica("99887766")
        recetas = historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)
    
    def test_emitir_receta_paciente_inexistente(self):

        self.clinica.agregar_medico(self.medico1)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("99999999", "MP201", ["Aspirina"])
    
    def test_emitir_receta_medico_inexistente(self):

        self.clinica.agregar_paciente(self.paciente1)
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.emitir_receta("99887766", "MP999", ["Aspirina"])
    
    def test_obtener_historia_clinica_paciente_inexistente(self):

        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_historia_clinica("99999999")
    
    def test_obtener_dia_semana_en_espanol(self):

        # Lunes 23 de junio de 2025
        fecha_lunes = datetime(2025, 6, 23)
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_lunes), "lunes")
        
        # Martes 24 de junio de 2025
        fecha_martes = datetime(2025, 6, 24)
        self.assertEqual(self.clinica.obtener_dia_semana_en_espanol(fecha_martes), "martes")
    
    def test_historia_clinica_contiene_turnos_y_recetas(self):

        # Configurar datos
        self.medico1.agregar_especialidad(self.especialidad_cardiologia)
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        # Agendar turno
        fecha = datetime(2025, 6, 23, 10, 0)  # Lunes
        self.clinica.agendar_turno("99887766", "MP201", "Cardiología", fecha)
        
        # Emitir receta
        self.clinica.emitir_receta("99887766", "MP201", ["Aspirina"])
        
        # Verificar historia clínica
        historia = self.clinica.obtener_historia_clinica("99887766")
        self.assertEqual(len(historia.obtener_turnos()), 1)
        self.assertEqual(len(historia.obtener_recetas()), 1)
    
    def test_emitir_receta_sin_medicamentos(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("99887766", "MP201", [])
            
if __name__ == '__main__':
    # Configurar el runner de tests para mostrar más detalles
    unittest.main(verbosity=2)