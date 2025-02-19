class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0
        self.temp_count = 0
        self.variable_table = {}
        
    def emit(self, op, arg1=None, arg2=None, result=None):
        self.code.append((op, arg1, arg2, result))
    
    def new_label(self):
        self.label_count += 1
        return f"__label{self.label_count}"
    
    def new_temp(self):
        self.temp_count += 1
        return f"__temp{self.temp_count}"
    
    def add_variable(self, name, var_type):
        if name in self.variable_table:
            raise ValueError(f"Variável {name} já declarada")
        default_value = 0 if var_type == 'int' else 0.0 if var_type == 'float' else ''
        self.variable_table[name] = {'type': var_type, 'address': len(self.variable_table)}
        self.emit('=', name, default_value, None)  # Emitir inicialização
    
    def get_code(self):
        return self.code

    def emit_label(self, label):
        self.code.append(('LABEL', label, None, None))