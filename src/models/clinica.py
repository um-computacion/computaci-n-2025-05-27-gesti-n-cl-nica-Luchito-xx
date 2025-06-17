from datetime import datetime

from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.turno import Turno
from src.models.historiaClinica import HistoriaClinica
from src.models.receta import Receta

from src.exceptions.error import (
    DatoInvalidoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    MedicoNoEncontradoException,
    PacienteNoEncontradoException
)

class Clinica:
    
    def __init__(self):

        self.__pacientes__: dict[str, Paciente] = {}
        self.__medicos__: dict[str, Medico] = {}
        self.__turnos__: list[Turno] = []
        self.__historias_clinicas__: dict[str, HistoriaClinica] = {}
    
    # Registro y acceso

    def agregar_paciente(self, paciente: Paciente):

        dni = paciente.obtener_dni()
        if dni in self.__pacientes__:
            raise DatoInvalidoException(f"Ya existe un paciente con DNI {dni}")
        
        self.__pacientes__[dni] = paciente
        
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)
    
    def agregar_medico(self, medico: Medico):

        matricula = medico.obtener_matricula()
        if matricula in self.__medicos__:
            raise DatoInvalidoException(f"Ya existe un medico con matricula {matricula}")
        
        self.__medicos__[matricula] = medico
    
    def obtener_pacientes(self) -> list[Paciente]:

        return list(self.__pacientes__.values())
    
    def obtener_medicos(self) -> list[Medico]:

        return list(self.__medicos__.values())
    
    def obtener_medico_por_matricula(self, matricula: str) -> Medico:

        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException(f"No se encontro medico con matricula {matricula}")
        return self.__medicos__[matricula]
    
    #Turno

    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        self.validar_turno_no_duplicado(matricula, fecha_hora)
        
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)

        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)
        
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos__.append(turno)
        
        historia_clinica = self.__historias_clinicas__[dni]
        historia_clinica.agregar_turno(turno)
    
    def obtener_turnos(self) -> list[Turno]:
        return self.__turnos__.copy()

    #Validar y utilidades

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):

        for turno in self.__turnos__:
            if (turno.obtener_medico().obtener_matricula() == matricula and 
                turno.obtener_fecha_hora() == fecha_hora):
                raise TurnoOcupadoException(f"El medico ya tiene un turno agendado en esa fecha y hora")
    
    def validar_existencia_paciente(self, dni: str):

        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException(f"No se encontro paciente con DNI {dni}")
    
    def validar_existencia_medico(self, matricula: str):

        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException(f"No se encontro medico con matricula {matricula}")
    
    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada: str, dia_semana: str):

        especialidades = medico.obtener_especialidades()
        for especialidad in especialidades:
            if (especialidad.obtener_especialidad().lower() == especialidad_solicitada.lower() and
                especialidad.verificar_dia(dia_semana)):
                return
        
        raise MedicoNoDisponibleException(
            f"El medico no atiende {especialidad_solicitada} el dia {dia_semana}"
        )
    
    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

        return dias[fecha_hora.weekday()]
    
    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str:

        especialidad = medico.obtener_especialidad_para_dia(dia_semana)
        if not especialidad:
            raise MedicoNoDisponibleException(f"El medico no atiende el dia {dia_semana}")
        return especialidad
    
    #Receta e historia clinica

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        
        receta = Receta(paciente, medico, medicamentos)
        
        historia_clinica = self.__historias_clinicas__[dni]
        historia_clinica.agregar_receta(receta)

    def obtener_historia_clinica(self, dni: str) -> HistoriaClinica:

        self.validar_existencia_paciente(dni)
        return self.__historias_clinicas__[dni]

    