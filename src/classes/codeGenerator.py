from classes.ast import *

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0
        self.temp_count = 0
        self.current_vars = {}

    def generate(self, node):
        self.visit(node)
        return self.code

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        method(node)

    def generic_visit(self, node):
        raise Exception(f'Nenhum método para visitar o nó {type(node).__name__}')

    def new_label(self):
        return f'__label{self.label_count}'

    def new_temp(self):
        return f'__temp{self.temp_count}'

    # ---- Métodos Principais Corrigidos ----
    def visit_ProgramNode(self, node):
        for func in node.functions:
            self.visit(func)

    def visit_FunctionNode(self, node):
        self.current_vars = {}
        self.visit(node.body)

    def visit_BlockNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_declarationNode(self, node):
        for var in node.identifier:
            var_name = f"{var.name}_0"
            self.current_vars[var.name] = var_name
            self.code.append(('=', var_name, 0, None))

    def visit_IoNode(self, node):
        if node.op == "out":
            if isinstance(node.types, LiteralNode):
                value = node.types.value.strip('"')
                self.code.append(('CALL', 'PRINT', value, None))
            else:
                var_name = self._get_var_name(node.types)
                self.code.append(('CALL', 'PRINT', None, var_name))
        elif node.op == "in":
            var_name = self._get_var_name(node.values)
            self.code.append(('CALL', 'SCAN', None, var_name))  # Corrigido: 4º elemento é a variável

    def visit_WhileNode(self, node):
        start_label = self.new_label()
        exit_label = self.new_label()
        
        self.code.append(('LABEL', start_label, None, None))
        cond_temp = self._process_condition(node.condition)
        self.code.append(('IF', cond_temp, exit_label, start_label))
        
        self.visit(node.body)
        self.code.append(('JUMP', start_label, None, None))
        self.code.append(('LABEL', exit_label, None, None))

    def visit_IfNode(self, node):
        true_label = self.new_label()
        false_label = self.new_label()
        end_label = self.new_label()

        cond_temp = self._process_condition(node.condition)
        self.code.append(('IF', cond_temp, true_label, false_label))

        self.code.append(('LABEL', true_label, None, None))
        self.visit(node.body)
        self.code.append(('JUMP', end_label, None, None))

        self.code.append(('LABEL', false_label, None, None))
        if node.else_body:
            self.visit(node.else_body)
        self.code.append(('LABEL', end_label, None, None))

    def visit_AssignmentNode(self, node):
        target = f"{node.identifier}_0"
        value = self._process_expression(node.value)
        self.code.append(('=', target, value, None))

    def visit_BinaryOpNode(self, node):
        left = self._resolve_operand(node.left)
        right = self._resolve_operand(node.right)
        temp = self.new_temp()
        self.code.append((node.op, temp, left, right))
        return temp

    # ---- Métodos Auxiliares ----
    def _get_var_name(self, node):
        if isinstance(node, VariableNode):
            return f"{node.name}_0"
        elif isinstance(node, str):  # Caso o valor seja passado como string
            return f"{node}_0"
        return None

    def _process_condition(self, node):
        return self.visit(node)

    def _process_expression(self, node):
        return self.visit(node)

    def _resolve_operand(self, node):
        if isinstance(node, VariableNode):
            return self._get_var_name(node)
        elif isinstance(node, LiteralNode):
            return node.value
        return None