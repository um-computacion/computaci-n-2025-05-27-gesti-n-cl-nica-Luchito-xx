# 🏥 Sistema de Gestión Clínica

Un sistema de gestión clinica desarrollado en Python que permite administrar pacientes, médicos, turnos y recetas médicas, utilizando POO.

## 📁 Estructura del Proyecto

```
clinica/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── paciente.py
│   │   ├── medico.py
│   │   ├── especialidad.py
│   │   ├── turno.py
│   │   ├── receta.py
│   │   ├── historiaClinica.py
│   │   └── clinica.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── error.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_clinica.py
│   ├── test_especialidades.py
│   ├── test_historiaClinica.py
│   ├── test_medico.py
│   ├── test_paciente.py
│   ├── test_recetas.py
│   └── test_turnos.py
├── DOCUMENTATION.md
└── README.md
```

## 🚀 Cómo Ejecutar el Sistema

### 📋 Requisitos
- Python 3.8 o superior

### ▶️ Ejecución
1. Navegue al directorio raíz del proyecto:

2. Ejecute el sistema:
   ```bash
   python -m src.cli
   ```

3. Siga las instrucciones del menú interactivo para:
   - Agregar pacientes y médicos
   - Configurar especialidades médicas
   - Agendar turnos
   - Emitir recetas
   - Consultar historias clínicas

## 🧪 Cómo Ejecutar las Pruebas

### ▶️ Ejecutar todas las pruebas
```bash
python -m unittest discover tests -v
```

### 🎯 Ejecutar pruebas específicas
```bash
# Pruebas de la clínica
python -m unittest tests.test_clinica -v

# Pruebas de pacientes
python -m unittest tests.test_paciente -v

# Pruebas de médicos
python -m unittest tests.test_medico -v

# Pruebas de especialidades
python -m unittest tests.test_especialidades -v

# Pruebas de turnos
python -m unittest tests.test_turnos -v

# Pruebas de recetas
python -m unittest tests.test_recetas -v

# Pruebas de historia clínica
python -m unittest tests.test_historiaClinica -v
```

## 🏗️ Explicación del Diseño General

### 🎯 Arquitectura del Sistema

El sistema está diseñado siguiendo principios de programación orientada a objetos con una arquitectura modular que separa claramente las responsabilidades:

#### 📊 Capa de Modelos (`src/models/`)
- **👤 Paciente**: Gestiona la información básica de los pacientes (nombre, DNI, fecha de nacimiento)
- **👨‍⚕️ Médico**: Administra los datos de los médicos y sus especialidades
- **🩺 Especialidad**: Define las especialidades médicas y los días de atención
- **📅 Turno**: Representa las citas médicas programadas
- **💊 Receta**: Gestiona las prescripciones médicas
- **📋 HistoriaClinica**: Mantiene el registro completo de turnos y recetas por paciente
- **🏥 Clinica**: Clase principal que coordina todas las operaciones del sistema

#### ⚠️ Capa de Excepciones (`src/exceptions/`)
- **error.py**: Define excepciones personalizadas para el manejo de errores específicos del dominio

#### 💻 Capa de Interfaz (`src/`)
- **cli.py**: Interfaz de línea de comandos que proporciona un menú interactivo

### ✨ Características Principales

1. **👥 Gestión de Pacientes**: Registro con validación de datos y formato de fechas
2. **👨‍⚕️ Gestión de Médicos**: Control de matrículas únicas y múltiples especialidades
3. **📅 Sistema de Turnos**: Validación de disponibilidad médica por día y especialidad
4. **💊 Recetas Médicas**: Emisión y almacenamiento de prescripciones
5. **📋 Historias Clínicas**: Registro completo de la atención médica por paciente

### ✅ Validaciones Implementadas

- **📝 Datos obligatorios**: Nombres, DNI, matrículas no pueden estar vacíos
- **📅 Fechas**: Formato correcto y validación de fechas futuras
- **🩺 Disponibilidad médica**: Verificación de especialidad y día de atención
- **🚫 Duplicados**: Prevención de pacientes, médicos y turnos duplicados
- **🔗 Integridad**: Validación de referencias entre entidades

### ⚠️ Manejo de Errores

El sistema implementa un sistema robusto de manejo de excepciones:
- Validación de entrada de datos
- Mensajes de error descriptivos
- Recuperación elegante de errores

### 🧪 Cobertura de Pruebas

Las pruebas unitarias cubren:
- Casos de uso exitosos
- Validaciones de datos inválidos
- Manejo de excepciones
- Integridad referencial
- Funcionalidades específicas de cada módulo

Este diseño garantiza un sistema mantenible, extensible y confiable para la gestión de una clínica médica.