class ASTNode:
    def __repr__(self):
        return f'{self.__class__.__name__}: '

class ProgramNode(ASTNode):
    def __init__(self, functions):
        self.functions = functions
    def __repr__(self):
        return super().__repr__() + f'({self.functions})'

class FunctionNode(ASTNode):
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params 
        self.body = body
    def __repr__(self):
        return super().__repr__() + f'(return_type = "{self.return_type}",\nname = "{self.name}",\nparams = "{self.params}",\nbody = "{self.body}")'

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return super().__repr__() + f'({self.statements})'

class AssignmentNode(ASTNode):
    def __init__(self, identifier, op, value):
        self.identifier = identifier
        self.op = op  # '=', '+=', etc.
        self.value = value
    def __repr__(self):
        return super().__repr__() + f'(identifier = "{self.identifier}",\nop = "{self.op}",\nvalue = "{self.value}")'

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return super().__repr__() + f'(left = "{self.left}",\nop = "{self.op}",\nright = "{self.right}")'

class declarationNode(ASTNode): 
    def __init__(self, type, identifier):
        self.type = type
        self.identifier = identifier
    def __repr__(self):
        return super().__repr__() + f'(type = "{self.type}",\nidentifiers = "{self.identifier}")'

class LiteralNode(ASTNode):
    def __init__(self, value, type):
        self.value = value
        self.type = type  # 'int', 'float', etc.
    def __repr__(self):
        return super().__repr__() + f'(value = "{self.value}",\ntype = "{self.type}")'

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return super().__repr__() + f'(name = "{self.name}")'

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return super().__repr__() + f'(condition = "{self.condition}",\nbody = "{self.body}")'

class ForNode(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body
    def __repr__(self):
        return super().__repr__() + f'(init = "{self.init}",\ncondition = "{self.condition}",\nupdate = "{self.update}",\nbody = "{self.body}")'

class IoNode(ASTNode):
    def __init__(self, op, types=[], values=[]):
        self.op = op
        self.types = types
        self.values = values
    def __repr__(self):
        return super().__repr__() + f'(op = "{self.op}",\ntypes = "{self.types}",\nvalues = "{self.values}")'

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
    def __repr__(self):
        return super().__repr__() + f'(condition = "{self.condition}",\nbody = "{self.body}",\nelse_body = "{self.else_body}")'