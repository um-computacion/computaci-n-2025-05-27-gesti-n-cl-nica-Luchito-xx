# Sistema de Gestión Clínica

## Cómo ejecutar el sistema

- Ejecute archivo en raiz de proyecto: 

```bash
python3 main.py
```

El sistema iniciará con un menú interactivo que permite:
- Agregar pacientes y médicos
- Agendar turnos
- Emitir recetas
- Ver historias clínicas
- Gestionar especialidades médicas

## Cómo ejecutar las pruebas

- Ejecute archivos en raiz del proyecto
```bash
# Ejecutar todas las pruebas
python3 -m pytest tests/

# Ejecutar pruebas específicas
python3 -m pytest tests/"nombre_archivo.py"
```

## Diseño General

### Arquitectura
El sistema sigue un patrón de **arquitectura por capas** con separación clara de responsabilidades:

- **Capa de Presentación**: `cli.py` - Interfaz de usuario por consola
- **Capa de Lógica de Negocio**: `models/clinica.py` - Coordinador principal del sistema
- **Capa de Modelos**: Entidades del dominio (`paciente.py`, `medico.py`, etc.)
- **Capa de Excepciones**: Manejo centralizado de errores

### Características del Diseño

- **Encapsulación**: Atributos privados con métodos de acceso
- **Validación Robusta**: Verificación de datos en constructores
- **Manejo de Excepciones**: Tipos específicos de errores del dominio
- **Separación de Responsabilidades**: Cada clase tiene un propósito específico

### Flujo Típico de Uso

1. Registrar médicos con sus especialidades y días de atención
2. Registrar pacientes (se crea historia clínica automáticamente)
3. Agendar turnos validando disponibilidad médica
4. Emitir recetas que se agregan a la historia clínica
5. Consultar información consolidada del sistema