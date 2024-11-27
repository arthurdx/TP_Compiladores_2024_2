from functions import *   
from sintax import *      
import sys

def main():
    if len(sys.argv) < 2:
        print("Passe o caminho do arquivo txt como argumento no terminal" + 
        "\nexemplo: python3 src/main.py <txt/arquivo.txt>")
        return

    filename = sys.argv[1]
    tokens = read_java_file(filename)
    print("Tokens gerados:", tokens)
    
    try:
        parse_program(tokens)
        print("Análise sintática concluída com sucesso.")
    except SyntaxError as e:
        print(f"Erro sintático: {e}")
    
if __name__ == '__main__':
    main()