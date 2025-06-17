from datetime import datetime
from src.models.clinica import Clinica
from src.models.paciente import Paciente
from src.models.especialidad import Especialidad
from src.models.medico import Medico
from src.exceptions.error import (
    DatoInvalidoException,
    EspecialidadInvalidaException,
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    MedicoNoEncontradoException,
    TurnoOcupadoException,
    RecetaInvalidaException
)


class CLI:
    def __init__(self):
        self.clinica = Clinica()
    
    def mostrar_menu(self):

        print("\n" + "#"*50)
        print("            SISTEMA DE GESTION CLINICA")
        print("#"*50)
        print("1) Agregar paciente")
        print("2) Agregar medico")
        print("3) Agendar turno")
        print("4) Agregar especialidad a medico")
        print("5) Emitir receta")
        print("6) Ver historia clinica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los medicos")
        print("0) Salir")
        print("#"*50)
    
    def solicitar_opcion(self) -> str:

        while True:
            try:
                opcion = input("Seleccione una opcion (0-9): ").strip()
                if opcion in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return opcion
                else:
                    print("\nOpcion invalida. Ingrese un numero del 0 al 9.\n")
            except KeyboardInterrupt:
                print("\n Nos vemos!!")
                return '0'
    
    def agregar_paciente(self):

        print("\n AGREGAR PACIENTE")
        print("*" * 50)
        
        try:
            nombre = input("Nombre completo: ").strip()
            dni = input("DNI: ").strip()
            fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ").strip()
            
            paciente = Paciente(nombre, dni, fecha_nacimiento)
            self.clinica.agregar_paciente(paciente)
            
            print(f"\nPaciente {nombre} agregado exitosamente.")
            
        except DatoInvalidoException as e:
            print(f"Error en los datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def agregar_medico(self):

        print("\n AGREGAR MEDICO")
        print("*" * 50)
        
        try:
            nombre = input("Nombre completo: ").strip()
            matricula = input("Matricula: ").strip()
            
            medico = Medico(nombre, matricula)
            
            print("\nAhora agregue las especialidades del medico:")
            while True:
                especialidad_nombre = input("\nNombre de la especialidad (o 'fin' para terminar): ").strip()
                if especialidad_nombre.lower() == 'fin':
                    break
                
                print("Dias de atencion (separados por comas):")
                print("\nOpciones: lunes, martes, miercoles, jueves, viernes, sabado, domingo")
                dias_input = input("Dias: ").strip()
                
                if dias_input:
                    dias = [dia.strip() for dia in dias_input.split(',')]
                    try:
                        especialidad = Especialidad(especialidad_nombre, dias)
                        medico.agregar_especialidad(especialidad)
                        print(f"\nEspecialidad {especialidad_nombre} agregada.")
                    except (DatoInvalidoException, EspecialidadInvalidaException) as e:
                        print(f"\nError en la especialidad: {e}")
            
            self.clinica.agregar_medico(medico)
            print(f"Medico {nombre} agregado exitosamente.")
            
        except DatoInvalidoException as e:
            print(f"Error en los datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def agendar_turno(self):
        print("\n  AGENDAR TURNO")
        print("*" * 50)
        
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matricula del medico: ").strip()
            especialidad = input("Especialidad solicitada: ").strip()
            

            fecha_str = input("Fecha del turno (dd/mm/aaaa): ").strip()
            hora_str = input("Hora del turno (HH:MM): ").strip()
            

            fecha_hora_str = f"{fecha_str} {hora_str}"
            fecha_hora = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
            
            self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            print("  Turno agendado exitosamente.")
            
        except ValueError as e:
            print("Error en el formato de fecha/hora. Usa dd/mm/aaaa HH:MM")
        except (PacienteNoEncontradoException, MedicoNoEncontradoException, 
                MedicoNoDisponibleException, TurnoOcupadoException) as e:
            print(f" {e}")
        except Exception as e:
            print(f" Error inesperado: {e}")
        pass
    
    def agregar_especialidad_medico(self):

        print("\n  AGREGAR ESPECIALIDAD A MEDICO")
        print("*" * 50)
        
        try:
            matricula = input("Matricula del medico: ").strip()
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            
            especialidad_nombre = input("Nombre de la especialidad: ").strip()
            print("Dias de atencion (separados por comas):")
            print("Opciones: lunes, martes, miercoles, jueves, viernes, sabado, domingo")
            dias_input = input("Dias: ").strip()
            
            dias = [dia.strip() for dia in dias_input.split(',')]
            especialidad = Especialidad(especialidad_nombre, dias)
            medico.agregar_especialidad(especialidad)
            
            print(f"\nEspecialidad {especialidad_nombre} agregada al medico.")
            
        except MedicoNoEncontradoException as e:
            print(f"{e}")
        except (DatoInvalidoException, EspecialidadInvalidaException) as e:
            print(f"Error en la especialidad: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def emitir_receta(self):
        print("\n  EMITIR RECETA")
        print("*" * 50)
        
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matricula del medico: ").strip()
            
            print("\nIngrese los medicamentos (escriba 'fin' para terminar):\n")
            medicamentos = []
            while True:
                medicamento = input("Medicamento: ").strip()
                if medicamento.lower() == 'fin':
                    break
                if medicamento:
                    medicamentos.append(medicamento)
            
            if not medicamentos:
                print("Debe ingresar al menos un medicamento.")
                return
            
            self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("\nReceta emitida exitosamente.\n")
            
        except (PacienteNoEncontradoException, MedicoNoEncontradoException) as e:
            print(f" {e}")
        except RecetaInvalidaException as e:
            print(f" Error en la receta: {e}")
        except Exception as e:
            print(f" Error inesperado: {e}")
    
    def ver_historia_clinica(self):

        print("\n  HISTORIA CLÍNICA")
        print("*" * 50)
        
        try:
            dni = input("DNI del paciente: ").strip()
            historia = self.clinica.obtener_historia_clinica(dni)
            print("\n" + str(historia))
            
        except PacienteNoEncontradoException as e:
            print(f"{e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def ver_todos_turnos(self):

        print("\n TODOS LOS TURNOS")
        print("*" * 50)
        
        turnos = self.clinica.obtener_turnos()
        if not turnos:
            print("No hay turnos agendados.")
            return
        
        for i, turno in enumerate(turnos, 1):
            print(f"{i}. {turno}")
    
    def ver_todos_pacientes(self):

        print("\n TODOS LOS PACIENTES")
        print("*" * 50)
        
        pacientes = self.clinica.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")
            return
        
        for i, paciente in enumerate(pacientes, 1):
            print(f"{i}. {paciente}")
    
    def ver_todos_medicos(self):

        print("\n TODOS LOS MEDICOS")
        print("*" * 50)
        
        medicos = self.clinica.obtener_medicos()
        if not medicos:
            print("No hay medicos registrados.")
            return
        
        for i, medico in enumerate(medicos, 1):
            print(f"{i}. {medico}")
            print()
    
    def ejecutar(self):

        print("\nNos alegramos de volver a verlo")
        
        while True:
            try:
                self.mostrar_menu()
                opcion = self.solicitar_opcion()
                
                if opcion == '0':
                    print("\n Sesion cerrada")
                    break
                elif opcion == '1':
                    self.agregar_paciente()
                elif opcion == '2':
                    self.agregar_medico()
                elif opcion == '3':
                    self.agendar_turno()
                elif opcion == '4':
                    self.agregar_especialidad_medico()
                elif opcion == '5':
                    self.emitir_receta()
                elif opcion == '6':
                    self.ver_historia_clinica()
                elif opcion == '7':
                    self.ver_todos_turnos()
                elif opcion == '8':
                    self.ver_todos_pacientes()
                elif opcion == '9':
                    self.ver_todos_medicos()

                if opcion != '0':
                    input("\nPresione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n Nos vemos!!")
                break
            except Exception as e:
                print(f"\nError inesperado en el sistema: {e}")
                input("Presione Enter para continuar...")


def main():

    cli = CLI()
    cli.ejecutar()


if __name__ == "__main__":
    main()