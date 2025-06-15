from datetime import datetime
from modelo import (
    Clinica, Paciente, Medico, Especialidad,
    MedicoNoEncontradoException, EspecialidadInvalidaException,
    DatoInvalidoException)


class CLI:
    def __init__(self):
        self.clinica = Clinica()
    
    def mostrar_menu(self):

        print("\n" + "="*50)
        print("            SISTEMA DE GESTION CLINICA")
        print("="*50)
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
        print("="*50)
    
    def solicitar_opcion(self) -> str:

        while True:
            try:
                opcion = input("Seleccione una opcion (0-9): ").strip()
                if opcion in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return opcion
                else:
                    print("Opcion invalida. Ingrese un numero del 0 al 9.")
            except KeyboardInterrupt:
                print("\n Nos vemos!!")
                return '0'
    
    def agregar_paciente(self):

        print("\n AGREGAR PACIENTE")
        print("-" * 30)
        
        try:
            nombre = input("Nombre completo: ").strip()
            dni = input("DNI: ").strip()
            fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ").strip()
            
            paciente = Paciente(nombre, dni, fecha_nacimiento)
            self.clinica.agregar_paciente(paciente)
            
            print(f"Paciente {nombre} agregado exitosamente.")
            
        except DatoInvalidoException as e:
            print(f"Error en los datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def agregar_medico(self):

        print("\n AGREGAR MEDICO")
        print("-" * 30)
        
        try:
            nombre = input("Nombre completo: ").strip()
            matricula = input("Matricula: ").strip()
            
            medico = Medico(nombre, matricula)
            
            print("\nAhora agregue las especialidades del medico:")
            while True:
                especialidad_nombre = input("Nombre de la especialidad (o 'fin' para terminar): ").strip()
                if especialidad_nombre.lower() == 'fin':
                    break
                
                print("Dias de atencion (separados por comas):")
                print("Opciones: lunes, martes, miercoles, jueves, viernes, sabado, domingo")
                dias_input = input("Dias: ").strip()
                
                if dias_input:
                    dias = [dia.strip() for dia in dias_input.split(',')]
                    try:
                        especialidad = Especialidad(especialidad_nombre, dias)
                        medico.agregar_especialidad(especialidad)
                        print(f"Especialidad {especialidad_nombre} agregada.")
                    except (DatoInvalidoException, EspecialidadInvalidaException) as e:
                        print(f"Error en la especialidad: {e}")
            
            self.clinica.agregar_medico(medico)
            print(f"Medico {nombre} agregado exitosamente.")
            
        except DatoInvalidoException as e:
            print(f"Error en los datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def agendar_turno(self):

        pass
    
    def agregar_especialidad_medico(self):

        print("\n  AGREGAR ESPECIALIDAD A MEDICO")
        print("-" * 40)
        
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
            
            print(f"Especialidad {especialidad_nombre} agregada al medico.")
            
        except MedicoNoEncontradoException as e:
            print(f"{e}")
        except (DatoInvalidoException, EspecialidadInvalidaException) as e:
            print(f"Error en la especialidad: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def emitir_receta(self):

        pass
    
    def ver_historia_clinica(self):

        pass
    
    def ver_todos_turnos(self):

        pass
    
    def ver_todos_pacientes(self):

        print("\n TODOS LOS PACIENTES")
        print("-" * 30)
        
        pacientes = self.clinica.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")
            return
        
        for i, paciente in enumerate(pacientes, 1):
            print(f"{i}. {paciente}")
    
    def ver_todos_medicos(self):

        print("\n TODOS LOS MeDICOS")
        print("-" * 30)
        
        medicos = self.clinica.obtener_medicos()
        if not medicos:
            print("No hay medicos registrados.")
            return
        
        for i, medico in enumerate(medicos, 1):
            print(f"{i}. {medico}")
            print()
    
    def ejecutar(self):

        print("            SISTEMA DE GESTION CLINICA")
        
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