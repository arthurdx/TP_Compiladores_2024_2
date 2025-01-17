from utils import *

class Interpreter():
    def __init__(self, calls):
        self.calls = calls
        self.variables = {}
    
    def exec(self, instruction):
        op, dest, reg1, reg2 = instruction
        try:
            reg1 = float(reg1)      
            reg2 = float(reg2)
        except ValueError:
            print("Operadores tem que ser números")
            return
        