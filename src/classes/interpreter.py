from utils import *

NEW_LINE = '\n'

class Interpreter():
    def __init__(self, filename):
        self.instructions = []
        self.labels = {}
        self.current_instruction = 0
        self.variables = {}
        self.running = True
        
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                instruction = eval(line.strip(f', \n'))
                if isinstance(instruction, tuple):
                    self.instructions.append(instruction)
                else:
                    raise ValueError(f"Instrução inválida: {line.strip(', {NEW_LINE}')}")
    
    def exec(self, instruction):
        for instruction in self.instructions:
            op, dest, reg1, reg2 = instruction
            try:
                reg1 = float(reg1)      
                reg2 = float(reg2)
            except ValueError:
                print("Operadores tem que ser números")
                return
    


        