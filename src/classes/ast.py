class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, functions):
        self.functions = functions

class FunctionNode(ASTNode):
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params 
        self.body = body  

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class AssignmentNode(ASTNode):
    def __init__(self, identifier, op, value):
        self.identifier = identifier
        self.op = op  # '=', '+=', etc.
        self.value = value

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class LiteralNode(ASTNode):
    def __init__(self, value, type):
        self.value = value
        self.type = type  # 'int', 'float', etc.

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body