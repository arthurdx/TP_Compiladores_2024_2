from functions import *   
from classes.parser import Parser    
import sys
import traceback
from classes.interpreter import Interpreter
from classes.codeGenerator import CodeGenerator

def main():
    if len(sys.argv) < 3:
        print("Passe o caminho do arquivo txt como argumento no terminal" + 
        "\nexemplo: python3 src/main.py <txt/arquivo.txt>")
        return
    
    filename = sys.argv[1]
    mode = int(sys.argv[2])
    
    
    if mode == 0:
        try:
            tokens = read_java_file(filename)
            print("Tokens gerados:", tokens)
        except Exception as e:
            print(f"Erro léxico: {e}")
        try:
            parser = Parser(tokens)
            ast_root = parser.parse_function()
            print("Código sintaticamente correto")
            generator = CodeGenerator()
            print(ast_root)
            intermediate_code = generator.generate(ast_root)
        except SyntaxError as e:
            print(f"Erro sintático: {e}")
        try:
            print("Código intermediário gerado: " )
            for instr in intermediate_code:
                print(instr)
            interpreter = Interpreter(code=intermediate_code)
            interpreter.execute()
        except Exception as e:
            print(f"Erro de execução: {e}")
    
    if mode == 1:
        interpreter = Interpreter(filename=filename)
        interpreter.execute()
    
if __name__ == '__main__':
    main()