import argparse
import os
from src import run_lexer, run_parser, run_interpreter, run_interpreter_with_file

def preprocess_file_path(file_path):
    """
    Normaliza y ajusta la ruta del archivo para evitar problemas con barras.
    """
    # Convierte a una ruta absoluta y normaliza
    file_path = os.path.abspath(file_path)
    # Asegúrate de reemplazar las barras invertidas si es necesario
    return file_path.replace("\\", "/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intérprete y ejecutor de archivos para el lenguaje OPL.")
    parser.add_argument(
        "file_path",
        nargs="?",  # Argumento opcional
        help="Ruta del archivo a ejecutar",
        default=None
    )
    
    args = parser.parse_args()

    if args.file_path:
        # Preprocesar la ruta del archivo
        file_path = preprocess_file_path(args.file_path)
        run_interpreter_with_file(file_path)
    else:
        run_interpreter()
