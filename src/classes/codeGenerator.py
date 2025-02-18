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
        