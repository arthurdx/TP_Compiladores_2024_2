class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_memory = 0
        self.temp_memory = 0
        self.variable_table = {}
    
    def emit(self, op, *operands):
        """Adiciona instrução ao código intermediário"""
        self.code.append((op,) + operands)

    def create_label(self):
        """Cria um label único"""
        label = f"__label{self.label_memory}"
        self.label_memory += 1
    
    def create_temp(self):
        """Gera uma variavel temporaria para calculos intermediarios"""
        temp = f"__temp{self.temp_memory}"
        self.temp_memory += 1
        return temp
    
    def new_variable(self, name, type):
        """Adiciona uma nova variável à tabela de variáveis"""
        if name in self.variable_table:
            raise ValueError(f"Variável {name} já foi declarada.")
        self.variable_table[name] = {"type": type, "address": len(self.variable_table)}

    def get_code(self):
        """Retorna o código intermediário gerado"""
        return self.code
    
    
        