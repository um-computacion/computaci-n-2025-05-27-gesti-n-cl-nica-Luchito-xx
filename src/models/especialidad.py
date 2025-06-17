from src.exceptions.error import DatoInvalidoException

class Especialidad:

    def __init__(self, tipo: str, dias: list[str]):

        if not tipo or not tipo.strip():
            raise DatoInvalidoException("El tipo de especialidad no puede estar vacio")
        if not dias or len(dias) == 0:
            raise DatoInvalidoException("Debe especificar al menos un dia de atencion")
        
        dias_validos = {'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'}
        dias_normalizados = []
        
        for dia in dias:
            dia_normalizado = self._normalizar_dia(dia.strip().lower())
            if dia_normalizado not in dias_validos:
                raise DatoInvalidoException(f"Dia invalido: {dia}. Dias validos: {', '.join(dias_validos)}")
            if dia_normalizado not in dias_normalizados:
                dias_normalizados.append(dia_normalizado)
        
        self.__tipo__ = tipo.strip()
        self.__dias__ = dias_normalizados
    
    def _normalizar_dia(self, dia: str) -> str:
        reemplazos = {
            'á': 'a', 'é': 'e', 'í': 'i',
            'ó': 'o', 'ú': 'u',
            'Á': 'a', 'É': 'e', 'Í': 'i',
            'Ó': 'o', 'Ú': 'u'
        }
        dia_sin_tildes = ''.join(reemplazos.get(c, c) for c in dia)
        return dia_sin_tildes.lower()

    def obtener_especialidad(self) -> str:

        return self.__tipo__
    
    def verificar_dia(self, dia: str) -> bool:

        return self._normalizar_dia(dia.strip().lower()) in self.__dias__
    
    def __str__(self) -> str:
        dias_str = ", ".join(self.__dias__)
        return f"{self.__tipo__} (Dias: {dias_str})"
