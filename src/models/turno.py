from src.models.paciente import Paciente
from src.models.medico import Medico
from src.exceptions.error import DatoInvalidoException
from datetime import datetime

class Turno:

    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str):

        if not isinstance(paciente, Paciente):
            raise DatoInvalidoException("Debe proporcionar un paciente valido")
        if not isinstance(medico, Medico):
            raise DatoInvalidoException("Debe proporcionar un medico valido")
        if not isinstance(fecha_hora, datetime):
            raise DatoInvalidoException("Debe proporcionar una fecha y hora valida")
        if fecha_hora < datetime.now():
            raise DatoInvalidoException("La fecha y hora del turno debe ser a futuro")
        if not especialidad or not especialidad.strip():
            raise DatoInvalidoException("Debe especificar una especialidad")
        
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha_hora__ = fecha_hora
        self.__especialidad__ = especialidad.strip()
    
    def obtener_medico(self) -> Medico:

        return self.__medico__
    
    def obtener_fecha_hora(self) -> datetime:

        return self.__fecha_hora__
    
    def obtener_paciente(self) -> Paciente:

        return self.__paciente__
    
    def obtener_especialidad(self) -> str:

        return self.__especialidad__
    
    def __str__(self) -> str:

        fecha_str = self.__fecha_hora__.strftime("%d/%m/%Y %H:%M")
        return f"Turno: {self.__paciente__.obtener_dni()} con Dr/a. {self.__medico__.obtener_matricula()} - {self.__especialidad__} el {fecha_str}"


