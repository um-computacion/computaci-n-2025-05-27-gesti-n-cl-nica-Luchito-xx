from src.models.paciente import Paciente
from src.models.turno import Turno
from src.models.receta import Receta

from src.exceptions.error import (
    DatoInvalidoException
)
class HistoriaClinica:

    def __init__(self, paciente: Paciente):
        
        if not isinstance(paciente, Paciente):
            raise DatoInvalidoException("Debe proporcionar un paciente valido")
        
        self.__paciente__ = paciente
        self.__turnos__: list[Turno] = []
        self.__recetas__: list[Receta] = []
    
    def agregar_turno(self, turno: Turno):

        if not isinstance(turno, Turno):
            raise DatoInvalidoException("Debe proporcionar un turno valido")
        self.__turnos__.append(turno)
    
    def agregar_receta(self, receta: Receta):

        if not isinstance(receta, Receta):
            raise DatoInvalidoException("Debe proporcionar una receta valida")
        self.__recetas__.append(receta)
    
    def obtener_turnos(self) -> list[Turno]:

        return self.__turnos__.copy()
    
    def obtener_recetas(self) -> list[Receta]:

        return self.__recetas__.copy()
    
    def __str__(self) -> str:

        resultado = f"=== Historia Clinica de {self.__paciente__} ===\n\n"
        
        resultado += f"TURNOS ({len(self.__turnos__)}):\n"
        if self.__turnos__:
            for i, turno in enumerate(self.__turnos__, 1):
                resultado += f"{i}. {turno}\n"
        else:
            resultado += "No hay turnos registrados.\n"
        
        resultado += f"\nRECETAS ({len(self.__recetas__)}):\n"
        if self.__recetas__:
            for i, receta in enumerate(self.__recetas__, 1):
                resultado += f"{i}. {receta}\n"
        else:
            resultado += "No hay recetas registradas.\n"
        
        return resultado
