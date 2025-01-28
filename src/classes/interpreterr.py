NEW_LINE = '\n'

class Interpreter:
    def __init__(self, filename=None):
        self.memory = {}
        self.labels = {}
        self.instruction_pointer = 0
        self.instructions = []
        self.running = True

        if filename:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    instruction = eval(line.strip(', \n'))
                    if isinstance(instruction, tuple):
                        self.instructions.append(instruction)
                    else:
                        raise ValueError(f"Instrução inválida: {line.strip(', {NEW_LINE}')}")

    def execute(self):
        """Executa uma lista de instruções do código intermediário."""
        self.preprocess_labels()
        
        while self.running and self.instruction_pointer < len(self.instructions):
            instr = self.instructions[self.instruction_pointer]
            self.instruction_pointer += 1
            self.execute_instruction(instr)

    def preprocess_labels(self):
        """Armazena os rótulos (LABEL) e suas posições na lista de instruções."""
        for i, instr in enumerate(self.instructions):
            if instr[0] == "LABEL":
                self.labels[instr[1]] = i

    def execute_instruction(self, instr):
        """Executa uma única instrução."""
        op, guardar, operando1, operando2 = instr

        if op == "=":  
            self.memory[guardar] = self.resolve_operand(operando1)
        elif op in {"+", "-", "*", "/", "%", "//", "+", "-"}:  
            val1 = self.resolve_operand(operando1)
            val2 = self.resolve_operand(operando2) if operando2 else None
            self.memory[guardar] = self.perform_arithmetic_operation(op, val1, val2)
        elif op in {"||", "&&", "!", "==", "<>", ">", "<", ">=", "<="}:  
            val1 = self.resolve_operand(operando1)
            val2 = self.resolve_operand(operando2) if operando2 else None
            self.memory[guardar] = self.perform_logical_operation(op, val1, val2)
        elif op == "CALL":  
            self.handle_call(guardar, operando1, operando2)
        elif op == "IF":  
            cond = self.resolve_operand(guardar)
            if cond:
                if operando1 in self.labels:
                    self.instruction_pointer = self.labels[operando1]
            else:
                if operando2 is not None and operando2 in self.labels:
                    self.instruction_pointer = self.labels[operando2]
        elif op == "JUMP":  
            if guardar in self.labels:
                self.instruction_pointer = self.labels[guardar]
        elif op == "LABEL":  
            pass
        else:
            raise ValueError(f"Operação desconhecida: {op}")

    def perform_arithmetic_operation(self, op, val1, val2):
        """Executa operações aritméticas e unárias."""
        if op == "+":
            result = val1 + val2
        elif op == "-":
            result = val1 - val2
        elif op == "*":
            result = val1 * val2
        elif op == "/":
            result = val1 / val2
        elif op == "%":
            result = val1 % val2
        elif op == "//":
            result = val1 // val2
        elif op == "+" and val2 is None:  
            result = +val1
        elif op == "-" and val2 is None: 
            result = -val1
        else:
            raise ValueError(f"Operação aritmética desconhecida: {op}")
        
        return result

    def perform_logical_operation(self, op, val1, val2):
        """Executa operações lógicas e relacionais."""
        if op == "||":  
            result = val1 or val2
        elif op == "&&":  
            result = val1 and val2
        elif op == "!":  
            result = not val1
        elif op == "==":  
            result = val1 == val2
        elif op == "<>":  
            result = val1 != val2
        elif op == ">":  
            result = val1 > val2
        elif op == "<": 
            result = val1 < val2
        elif op == ">=":  
            result = val1 >= val2
        elif op == "<=":  
            result = val1 <= val2
        else:
            raise ValueError(f"Operação lógica ou relacional desconhecida: {op}")
        
        return result

    def handle_call(self, func, param1, param2):
        """Manipula chamadas de funções."""
        if func == "PRINT":
            value = self.memory[param2] if param2 is not None else param1
            print(value, end="")
        elif func == "SCAN":
            value = input()  
            self.memory[param2] = int(value) if value.isdigit() else value
        elif func == "STOP":
            self.running = False
        else:
            raise ValueError(f"Função desconhecida: {func}")

    def resolve_operand(self, operand, operand_type=None):
        """Resolve o valor de um operando."""
        if operand is None:
            return None
        if isinstance(operand, (int, float)):
            return operand
        if isinstance(operand, str) and operand.isdigit():
            return int(operand)
        elif operand in self.memory:
            return self.memory[operand]
        else:
            raise ValueError(f"Operando desconhecido: {operand}")