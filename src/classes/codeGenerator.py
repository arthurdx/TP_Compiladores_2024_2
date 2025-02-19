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
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'Nenhum método para visitar o nó {type(node).__name__}')

    def new_label(self):
        label = f'__label{self.label_count}'
        self.label_count += 1
        return label

    def new_temp(self):
        temp = f'__temp{self.temp_count}'
        self.temp_count += 1
        return temp

    # ------ Métodos principais corrigidos ------
    def visit_ProgramNode(self, node):
        for func in node.functions:
            self.visit(func)

    def visit_FunctionNode(self, node):
        self.current_vars = {}
        for stmt in node.body.statements:
            self.visit(stmt)
    
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
                var_name = self._resolve_variable(node.types)
                self.code.append(('CALL', 'PRINT', None, var_name))
        elif node.op == "in":
            var_name = self._resolve_variable(node.values)
            self.code.append(('CALL', 'SCAN', None, var_name))

    def visit_WhileNode(self, node):
        loop_start = self.new_label()
        loop_exit = self.new_label()
        
        # Label inicial
        self.code.append(('LABEL', loop_start, None, None))
        
        # Processar condição (ex: numBloco > 1)
        cond_temp = self._process_expression(node.condition)
        self.code.append(('IF', cond_temp, loop_exit, loop_start))  # Se falso, sai
        
        # Corpo do loop
        self.visit(node.body)
        self.code.append(('JUMP', loop_start, None, None))
        self.code.append(('LABEL', loop_exit, None, None))

    def visit_IfNode(self, node):
        true_label = self.new_label()
        false_label = self.new_label()
        end_label = self.new_label()

        cond_temp = self._process_expression(node.condition)
        self.code.append(('IF', cond_temp, true_label, false_label))

        # Bloco verdadeiro
        self.code.append(('LABEL', true_label, None, None))
        self.visit(node.body)
        self.code.append(('JUMP', end_label, None, None))

        # Bloco falso
        self.code.append(('LABEL', false_label, None, None))
        if node.else_body:
            self.visit(node.else_body)
        self.code.append(('LABEL', end_label, None, None))

    def visit_AssignmentNode(self, node):
        target_var = f"{node.identifier}_0"
        value_temp = self._process_expression(node.value)
        self.code.append(('=', target_var, value_temp, None))

    def visit_BinaryOpNode(self, node):
        left = self._resolve_operand(node.left)
        right = self._resolve_operand(node.right)
        temp = self.new_temp()
        self.code.append((node.op, temp, left, right))
        return temp  # Retorna o temporário para uso em outras operações

    # ------ Métodos auxiliares ------
    def _resolve_variable(self, node):
        if isinstance(node, VariableNode):
            return f"{node.name}_0"
        if isinstance(node, LiteralNode):
            return node.value
        return None

    def _process_expression(self, expr_node):
        if isinstance(expr_node, BinaryOpNode):
            return self.visit_BinaryOpNode(expr_node)
        elif isinstance(expr_node, VariableNode):
            return self._resolve_variable(expr_node)
        elif isinstance(expr_node, LiteralNode):
            return expr_node.value
        return None

    def _resolve_operand(self, operand):
        if isinstance(operand, VariableNode):
            return f"{operand.name}_0"
        elif isinstance(operand, LiteralNode):
            return operand.value
        return None