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
        
        nombre_limpio = nombre.strip()
        if len(nombre_limpio) > 50:
            raise DatoInvalidoException("El nombre del paciente no puede tener mas de 50 caracteres")

        for char in nombre_limpio:
            if not (char.isalpha() or char.isspace()):
                raise DatoInvalidoException("El nombre del paciente solo puede contener letras y espacios")
            
        dni_limpio = dni.strip()
        if len(dni_limpio) != 8:
            raise DatoInvalidoException("El DNI debe tener exactamente 8 caracteres")
        
        if not dni_limpio.isdigit():
            raise DatoInvalidoException("El DNI solo puede contener numeros")
         
        self.__nombre__= nombre_limpio
        self.__dni__ = dni_limpio
        self.__fecha_nacimiento__ = fecha_nacimiento.strip()
        self.__nombre__= nombre.strip()
        self.__dni__ = dni.strip()
        self.__fecha_nacimiento__ = fecha_nacimiento.strip()
    
    def obtener_dni(self) -> str:

        return self.__dni__
    
    def __str__(self) -> str:

        return f"Nombre del Paciente: {self.__nombre__} (DNI: {self.__dni__}, Nacimiento: {self.__fecha_nacimiento__})"
