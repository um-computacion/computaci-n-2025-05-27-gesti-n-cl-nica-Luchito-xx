from src.models.especialidad import Especialidad
from src.exceptions.error import (
    DatoInvalidoException,
    EspecialidadInvalidaException
)
class Medico:

    def __init__(self, nombre: str, matricula: str):

        if not nombre or not nombre.strip():
            raise DatoInvalidoException("El nombre del medico no puede estar vacio")
        if not matricula or not matricula.strip():
            raise DatoInvalidoException("La matricula del medico no puede estar vacia")
        
        self.__nombre__ = nombre.strip()
        self.__matricula__ = matricula.strip()
        self.__especialidades__: list[Especialidad] = []
    
    def agregar_especialidad(self, especialidad: Especialidad):

        for esp in self.__especialidades__:
            if esp.obtener_especialidad().lower() == especialidad.obtener_especialidad().lower():
                raise EspecialidadInvalidaException(f"El medico ya tiene la especialidad {especialidad.obtener_especialidad()}")
        
        self.__especialidades__.append(especialidad)
    
    def obtener_matricula(self) -> str:

        return self.__matricula__
    
    def obtener_especialidad_para_dia(self, dia: str) -> str | None:

        for especialidad in self.__especialidades__:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None
    
    def obtener_especialidades(self) -> list[Especialidad]:

        return self.__especialidades__.copy()
    
    def __str__(self) -> str:

        especialidades_str = ", ".join([str(esp) for esp in self.__especialidades__])
        return f"Dr/a. {self.__nombre__} (Matricula: {self.__matricula__})\nEspecialidades: {especialidades_str if especialidades_str else 'Ninguna'}"

