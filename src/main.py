from TokenMap import TokenMap
from utils import *
from functions import *
import sys

def main():
    print(len(sys.argv))
    if len(sys.argv) < 2:
        print("Passe o caminho do arquivo txt como argumento no terminal" + 
        "\nexemplo: python3 src/main.py <txt/arquivo.txt>")
        return
    filename = sys.argv[1]
    read_java_file(filename)

if __name__ == '__main__':
    main()
    
