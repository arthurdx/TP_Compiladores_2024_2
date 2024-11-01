from functions import *
import sys

def main():
    if len(sys.argv) < 2:
        print("Passe o caminho do arquivo txt como argumento no terminal" + 
        "\nexemplo: python3 src/main.py <txt/arquivo.txt>")
        return
    filename = sys.argv[1]
    output = read_java_file(filename)
    print(output)

if __name__ == '__main__':
    main()
    
