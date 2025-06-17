from datetime import datetime
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.exceptions.error import (
    RecetaInvalidaException
)
class Receta:

    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str]):

        if not isinstance(paciente, Paciente):
            raise DatoInvalidoException("Debe proporcionar un paciente valido")
        if not isinstance(medico, Medico):
            raise DatoInvalidoException("Debe proporcionar un medico valido")
        if not medicamentos or len(medicamentos) == 0:
            raise RecetaInvalidaException("Debe especificar al menos un medicamento")
        
        medicamentos_validos = [med.strip() for med in medicamentos if med and med.strip()]
        if not medicamentos_validos:
            raise RecetaInvalidaException("Debe especificar al menos un medicamento valido")
        
        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = medicamentos_validos
        self.__fecha = datetime.now()
    
    def obtener_paciente(self) -> Paciente:

        return self.__paciente
    
    def obtener_medico(self) -> Medico:

        return self.__medico
    
    def obtener_fecha(self) -> datetime:

        return self.__fecha
    
    def __str__(self) -> str:

        fecha_str = self.__fecha.strftime("%d/%m/%Y %H:%M")
        medicamentos_str = ", ".join(self.__medicamentos)
        return f"Receta del {fecha_str} - Dr/a. {self.__medico.obtener_matricula()} para {self.__paciente.obtener_dni()}: {medicamentos_str}"

