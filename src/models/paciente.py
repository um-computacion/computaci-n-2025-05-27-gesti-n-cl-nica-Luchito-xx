from datetime import datetime
from src.exceptions.error import (
    DatoInvalidoException
)
class Paciente:

    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):

        if not nombre or not nombre.strip():
            raise DatoInvalidoException("El nombre del paciente no puede estar vacio")
        if not dni or not dni.strip():
            raise DatoInvalidoException("El DNI del paciente no puede estar vacio")
        if not fecha_nacimiento or not fecha_nacimiento.strip():
            raise DatoInvalidoException("La fecha de nacimiento no puede estar vacia")

         
        try:
            fecha_nac_dt = datetime.strptime(fecha_nacimiento.strip(), "%d/%m/%Y")
        except ValueError:
            raise DatoInvalidoException("La fecha de nacimiento debe tener el formato dd/mm/aaaa")


        if fecha_nac_dt > datetime.now():
            raise DatoInvalidoException("La fecha de nacimiento no puede ser en el futuro")

        self.__nombre__= nombre.strip()
        self.__dni__ = dni.strip()
        self.__fecha_nacimiento__ = fecha_nacimiento.strip()
    
    def obtener_dni(self) -> str:

        return self.__dni__
    
    def __str__(self) -> str:

        return f"Nombre del Paciente: {self.__nombre__} (DNI: {self.__dni__}, Nacimiento: {self.__fecha_nacimiento__})"
