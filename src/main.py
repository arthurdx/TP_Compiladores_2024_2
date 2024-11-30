from functions import *   
from classes.parser import Parser    
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
        parser = Parser(tokens)
        parser.parse_function()
    except SyntaxError as e:
        print(f"Erro sintático: {e}")
    
if __name__ == '__main__':
    main()