from datetime import datetime

####### Paciente ####### 

class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):

        if not nombre or not nombre.strip():
            raise DatoInvalidoException("El nombre del paciente no puede estar vacio")
        if not dni or not dni.strip():
            raise DatoInvalidoException("El DNI del paciente no puede estar vacio")
        if not fecha_nacimiento or not fecha_nacimiento.strip():
            raise DatoInvalidoException("La fecha de nacimiento no puede estar vacia")
        
        self.__nombre__= nombre.strip()
        self.__dni__ = dni.strip()
        self.__fecha_nacimiento__ = fecha_nacimiento.strip()
    
    def obtener_dni(self) -> str:

        return self.__dni__
    
    def __str__(self) -> str:

        return f"Nombre del Paciente: {self.__nombre__} (DNI: {self.__dni__}, Nacimiento: {self.__fecha_nacimiento__})"


####### Especialidad ####### 

class Especialidad:
    def __init__(self, tipo: str, dias: list[str]):

        if not tipo or not tipo.strip():
            raise DatoInvalidoException("El tipo de especialidad no puede estar vacio")
        if not dias or len(dias) == 0:
            raise DatoInvalidoException("Debe especificar al menos un dia de atencion")
        
        dias_validos = {'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'}
        dias_normalizados = []
        
        for dia in dias:
            dia_normalizado = dia.strip().lower()
            if dia_normalizado not in dias_validos:
                raise DatoInvalidoException(f"Dia invalido: {dia}. Dias validos: {', '.join(dias_validos)}")
            if dia_normalizado not in dias_normalizados:
                dias_normalizados.append(dia_normalizado)
        
        self.__tipo__ = tipo.strip()
        self.__dias__ = dias_normalizados
    
    def obtener_especialidad(self) -> str:

        return self.__tipo__
    
    def verificar_dia(self, dia: str) -> bool:

        return dia.strip().lower() in self.__dias__
    
    def __str__(self) -> str:
        dias_str = ", ".join(self.__dias__)
        return f"{self.__tipo__} (Dias: {dias_str})"


####### Medico ####### 

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

        for espdad in self.__especialidades__:
            if espdad.obtener_especialidad().lower() == especialidad.obtener_especialidad().lower():
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


####### Turno ####### 

class Turno:
    pass

####### Receta####### 

class Receta:
    pass

####### HistoriaClinica ####### 

class HistoriaClinica:
    pass


####### Clinica ####### 

class Clinica:
    def __init__(self):

        self.__pacientes__: dict[str, Paciente] = {}
        self.__medicos__: dict[str, Medico] = {}
    
    def agregar_paciente(self, paciente: Paciente):

        dni = paciente.obtener_dni()
        if dni in self.__pacientes__:
            raise DatoInvalidoException(f"Ya existe un paciente con DNI {dni}")
        
        self.__pacientes__[dni] = paciente
    
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
    
    def obtener_paciente_por_dni(self, dni: str) -> Paciente:

        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException(f"No se encontro paciente con DNI {dni}")
        return self.__pacientes__[dni]
    
    def validar_existencia_paciente(self, dni: str):

        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException(f"No se encontro paciente con DNI {dni}")
    
    def validar_existencia_medico(self, matricula: str):

        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException(f"No se encontro medico con matricula {matricula}")
    
    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

        return dias[fecha_hora.weekday()]
    
    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str:

        especialidad = medico.obtener_especialidad_para_dia(dia_semana)
        if not especialidad:
            raise MedicoNoDisponibleException(f"El medico no atiende el dia {dia_semana}")
        return especialidad
    
    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada: str, dia_semana: str):

        especialidades = medico.obtener_especialidades()
        for especialidad in especialidades:
            if (especialidad.obtener_especialidad().lower() == especialidad_solicitada.lower() and
                especialidad.verificar_dia(dia_semana)):
                return
        
        raise MedicoNoDisponibleException(
            f"El medico no atiende {especialidad_solicitada} el dia {dia_semana}"
        )
    
####### Excepciones ####### 
class PacienteNoEncontradoException(Exception):
    pass

class MedicoNoEncontradoException(Exception):
    pass

class MedicoNoDisponibleException(Exception):
    pass

class EspecialidadInvalidaException(Exception):
    pass

class DatoInvalidoException(Exception):
    pass




class TurnoOcupadoException(Exception):
    pass

class RecetaInvalidaException(Exception):
    pass

