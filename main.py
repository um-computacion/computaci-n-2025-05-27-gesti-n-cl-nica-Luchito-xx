from src.models.clinica import Clinica
from src.cli import CLI

if __name__ == "__main__":
    clinica = Clinica()
    cli = CLI()

    cli.ejecutar()