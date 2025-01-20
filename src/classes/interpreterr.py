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
        
        print("Iniciando execução das instruções...")  # Verificação inicial

        while self.running and self.instruction_pointer < len(self.instructions):
            instr = self.instructions[self.instruction_pointer]
            print(f"Processando instrução: {instr}")  # Exibir a instrução atual
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
        
        # Log da instrução
        self.log(op, guardar, operando1, operando2)

        if op == "=":  # Atribuição
            self.memory[guardar] = self.resolve_operand(operando1)
        elif op in {"+", "-", "*", "/", "%", "//", "+", "-"}:  # Operações aritméticas
            val1 = self.resolve_operand(operando1)
            val2 = self.resolve_operand(operando2) if operando2 else None
            self.memory[guardar] = self.perform_arithmetic_operation(op, val1, val2)
        elif op in {"||", "&&", "!", "==", "<>", ">", "<", ">=", "<="}:  # Operações lógicas e relacionais
            val1 = self.resolve_operand(operando1)
            val2 = self.resolve_operand(operando2) if operando2 else None
            self.memory[guardar] = self.perform_logical_operation(op, val1, val2)
        elif op == "CALL":  # Chamadas de funções
            self.handle_call(guardar, operando1, operando2)
        elif op == "IF":  # Controle condicional
            cond = self.resolve_operand(guardar)
            self.instruction_pointer = self.labels[operando1] if cond else self.labels[operando2]
        elif op == "JUMP":  # Saltos incondicionais
            self.instruction_pointer = self.labels[guardar]
        elif op == "LABEL":  # Apenas um marcador, não faz nada
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
        elif op == "+" and val2 is None:  # Operação unária de adição
            result = +val1
        elif op == "-" and val2 is None:  # Operação unária de subtração
            result = -val1
        else:
            raise ValueError(f"Operação aritmética desconhecida: {op}")
        
        # Log do resultado da operação
        self.log_result(op, result)
        return result

    def perform_logical_operation(self, op, val1, val2):
        """Executa operações lógicas e relacionais."""
        if op == "||":  # OU lógico
            result = val1 or val2
        elif op == "&&":  # E lógico
            result = val1 and val2
        elif op == "!":  # NÃO lógico
            result = not val1
        elif op == "==":  # Igualdade
            result = val1 == val2
        elif op == "<>":  # Diferença
            result = val1 != val2
        elif op == ">":  # Maior que
            result = val1 > val2
        elif op == "<":  # Menor que
            result = val1 < val2
        elif op == ">=":  # Maior ou igual
            result = val1 >= val2
        elif op == "<=":  # Menor ou igual
            result = val1 <= val2
        else:
            raise ValueError(f"Operação lógica ou relacional desconhecida: {op}")
        
        # Log do resultado da operação
        self.log_result(op, result)
        return result

    def handle_call(self, func, param1, param2):
        """Manipula chamadas de funções."""
        if func == "PRINT":
            value = self.resolve_operand(param2 or param1)
            print(value, end="")
        elif func == "SCAN":
            value = input()  # Entrada do usuário
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
        elif operand in self.memory:
            return self.memory[operand]
        else:
            raise ValueError(f"Operando desconhecido: {operand}")

    def log(self, op, guardar, operando1, operando2):
        """Imprime no terminal o que a instrução está fazendo."""
        print(f"Executando operação: {op}")
        print(f"Guardar em: {guardar}")
        print(f"Operando 1: {operando1}")
        print(f"Operando 2: {operando2 if operando2 else 'N/A'}")

    def log_result(self, op, result):
        """Imprime o resultado da operação."""
        print(f"Resultado da operação '{op}': {result}")
