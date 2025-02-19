from utils import *
from classes.codeGenerator import CodeGenerator
from classes.ast import *

class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.pos = 0
        self.current_token = None
        self.code_generator = CodeGenerator()

    def set_current_token(self):
        """Define o token atual."""
        self.current_token = self.token_list[self.pos] if self.pos < len(self.token_list) else None

    def next_position(self):
        """Avanca para o proximo token."""
        if self.pos < len(self.token_list):
            self.pos += 1
            self.set_current_token()


    def get_token_name(self, token_value):
        """Obtem o nome do token a partir do token_map."""
        for key, value in token_map.items():
            if isinstance(value, dict):
                for _, v in value.items():
                    if v == token_value:
                        return key 
        return "Desconhecido"
        
    def consume(self, expected_type):
        """Verifica e consome o token atual se ele corresponder a um dos tipos esperados."""
        if not(self.current_token and self.current_token[0]) == expected_type:
            # Token nao corresponde, lanca erro 
            expected_name = self.get_token_name(expected_type)
            raise SyntaxError(
                f"Token inesperado '{self.current_token[1] if self.current_token else None}'. "
                f"Esperado: {expected_name}, "
                f"Na Linha: {self.current_token[2] if self.current_token else None} e na Coluna: {self.current_token[3] if self.current_token else None}."
            )
        # print(f"Token consumido: {self.current_token[1]}")
        self.next_position()

    def parse_function(self):
        """<function*> -> <type> 'IDENT' '(' ')' <bloco>'"""
        self.set_current_token()
        return_type = self.parse_type()
        func_name = self.current_token[1]
        self.consume(token_map['IDEN'])
        self.consume(token_map['(']['LPAR'])
        self.consume(token_map[')']['RPAR'])
        body = self.parse_bloco()
        if self.pos < len(self.token_list):
            raise SyntaxError(f"Token inesperado '{self.current_token[1] if self.current_token else None}', "
                              f"na linha '{self.current_token[2] if self.current_token else None}' e "
                              f"na coluna '{self.current_token[3] if self.current_token else None}'. Esperado: fim do arquivo.")
        return FunctionNode(return_type, func_name, [], body)
    
    def parse_type(self):
        """<type> -> 'int' | 'float' | 'string'"""
        f_type = self.current_token[0]
        if f_type == token_map['int']['KINT']:
            self.consume(token_map['int']['KINT'])
        elif f_type == token_map['float']['KFLT']:
            self.consume(token_map['float']['KFLT'])
        elif f_type == token_map['string']['KSTR']:    
            self.consume(token_map['string']['KSTR'])
        return f_type
        

    
    def parse_bloco(self):
        """<bloco> -> '{' <stmList> '}'"""
        self.consume(token_map['{']['LBRC'])
        stmts = self.parse_stmList()
        self.consume(token_map['}']['RBRC'])
        return BlockNode(stmts)

    def parse_stmList(self):
        """<stmList> -> <stm> <stmList> | &"""
        stmts = []
        if self.current_token and self.current_token[0] != token_map['}']['RBRC']:
            stmt = self.parse_stmt()
            stmts.append(stmt)
            stmts += self.parse_stmList()
        return stmts

    def parse_stmt(self):
        """
            <stmt> -> <forStmt> 
            | <ioStmt>
            | <whileStmt>
            | <atrib> ';' 
            | <ifStmt> 
            | <bloco> 
            | 'break'
            | 'continue'
            | <declaration>
            | ';' ;
        """
        if self.current_token[0] == token_map['for']['FOR']:
            return self.parse_forStmt()
        elif self.current_token[0] == token_map['system']['SYS']:
            return self.parse_ioStmt()
        elif self.current_token[0] == token_map['while']['WHL']:
            return self.parse_whileStmt()
        elif self.current_token[0] == token_map['IDEN']:
            node = self.parse_atrib()
            self.consume(token_map[';']['SMCL'])
            return node
        elif self.current_token[0] == token_map['if']['IF']:
            return self.parse_ifStmt()
        elif self.current_token[0] == token_map['{']['LBRC']:
            return self.parse_bloco()
        elif self.current_token[0] == token_map['break']['BRK']:
            self.consume(token_map['break']['BRK'])
            node = ASTNode()
            node.break_stmt = True
            return node
        elif self.current_token[0] == token_map['continue']['CTN']:
            self.consume(token_map['continue']['CTN'])
            node = ASTNode()
            node.continue_stmt = True
            return node
        elif self.current_token[0] in [token_map['int']['KINT'], token_map['float']['KFLT'], token_map['string']['KSTR']]:
            return self.parse_declaration()  
        elif self.current_token[0] == token_map[';']['SMCL']:
            self.consume(token_map[';']['SMCL'])
            return None
        elif self.current_token[0] == token_map['}']['RBRC']:
            self.consume(token_map['}']['RBRC'])
            return None
        

    def parse_forStmt(self):
        """<forStmt> -> 'for' '(' <optAtrib> ';' <optExpr> ';' <optAtrib> ')' <stmt> ;r"""
        self.consume(token_map['for']['FOR'])
        self.consume(token_map['(']['LPAR'])
        init = self.parse_optAtrib()
        self.consume(token_map[';']['SMCL'])
        condition = self.parse_optExpr()
        self.consume(token_map[';']['SMCL'])
        update = self.parse_optAtrib()
        self.consume(token_map[')']['RPAR'])
        body = self.parse_stmt()
        return ForNode(init, condition, update, body)
    

    def parse_optAtrib(self):
        """<optAtrib> -> <atrib> | & ;"""
        if self.current_token[0] == token_map['IDEN']:
            return self.parse_atrib()
        return None

    def parse_atrib(self):
        """
        <atrib> -> 'IDENT' '=' <expr> 
         | 'IDENT' '+=' <expr> 
         | 'IDENT' '-=' <expr> 
         | 'IDENT' '*=' <expr> 
         | 'IDENT' '/=' <expr> 
         | 'IDENT' '%=' <expr>;
        """
        ident = self.current_token[1]
        self.consume(token_map['IDEN'])
        op = self.current_token[1]
        if self.current_token[0] == token_map['=']['ASSG']:
            self.consume(token_map['=']['ASSG'])
        if self.current_token[0] == token_map['+=']['INC']:
            self.consume(token_map['+=']['INC'])
        if self.current_token[0] == token_map['-=']['DEC']:        
            self.consume(token_map['-=']['DEC'])
        if self.current_token[0] == token_map['*=']['ASMU']:
            self.consume(token_map['*=']['ASMU'])
        if self.current_token[0] == token_map['/=']['ASDV']:
            self.consume(token_map['/=']['ASDV'])
        if self.current_token[0] == token_map['%=']['ASMD']:
            self.consume(token_map['%=']['ASMD'])
        expr_node = self.parse_expr()
        return AssignmentNode(ident, op, expr_node)
    
    def parse_optExpr(self):
        """<optExpr> -> <expr> | & """
        if self.current_token[0] != token_map[';']['SMCL']:
            self.parse_expr()
        return None
                    

    def parse_expr(self):
        "<expr> -> <or> ;"
        return self.parse_or()

    def parse_or(self):
        """<or> -> <and> <restoOr> ;"""
        left_side = self.parse_and()
        return self.parse_resto_or(left_side)

    def parse_resto_or(self, left_side):
        """<restoOr> -> '||' <and> <restoOr> | & ;"""
        if self.current_token[0] == token_map['||']['OR']:
            op = self.current_token[1]
            self.consume(token_map['||']['OR'])
            right_side =  self.parse_and()
            new_left_side = BinaryOpNode(left_side, op, right_side)
            return self.parse_resto_or(new_left_side)
        return left_side   

    def parse_and(self):
        """<and> -> <not> <restoAnd> ;"""
        left_side = self.parse_not()
        return self.parse_resto_and(left_side)

    def parse_resto_and(self, left_side):
        """<restoAnd> -> '&&' <not> <restoAnd> | & ;"""
        if self.current_token[0] == token_map['&&']['AND']:
            op = self.current_token[1]
            self.consume(token_map['&&']['AND'])
            right_side = self.parse_not()    
            new_left_side = BinaryOpNode(left_side, op, right_side)
            return self.parse_resto_and(new_left_side)
        return left_side

    def parse_not(self):
        """<not> -> '!' <not> | <rel> ;"""
        if self.current_token[0] == token_map['!']['NOT']:
            op = self.current_token[1]
            self.consume(token_map['!']['NOT'])
            right_side = self.parse_not()  
            return BinaryOpNode(LiteralNode("!", "operator"), op, right_side)
        else:  
            return self.parse_rel()
        
    def parse_rel(self):
        """<rel> -> <add> <restoRel> ;"""
        left = self.parse_add()
        self.parse_resto_rel(left)

    def parse_resto_rel(self, left_side):
        """
        <restoRel> -> '==' <add> | '!=' <add>
                   | '<' <add> | '<=' <add> 
                   | '>' <add> | '>=' <add> | ε 
        """
        if self.current_token[0] in [token_map['==']['EQL'], token_map['!=']['DIF'], 
                                     token_map['>']['GT'], token_map['>=']['GET'], 
                                     token_map['<']['LT'], token_map['<=']['LET']]:
            op = self.current_token[1]
            self.consume(self.current_token[0])
            right_side = self.parse_add()
            new_left = BinaryOpNode(left_side, op, right_side)
            return self.parse_resto_rel(new_left)
        return left_side

    def parse_add(self):
        """<add> -> <mult> <restoAdd> ;"""
        left_side = self.parse_mult()
        return self.parse_resto_add(left_side)

    def parse_resto_add(self, left_side):
        """<restoAdd> -> '+' <mult> <restoAdd> 
            | '-' <mult> <restoAdd> | & ;""" 
        if self.current_token[0] in [token_map['+']['ADD'], token_map['-']['SUB']]:
            op = self.current_token[1]
            self.consume(self.current_token[0])
            right_side = self.parse_mult()
            new_left_side = BinaryOpNode(left_side, op, right_side)
            return self.parse_resto_add(new_left_side)
        return left_side

    def parse_mult(self):
        """<mult> -> <uno> <restoMult> ;"""
        left_side = self.parse_uno()
        return self.parse_resto_mult(left_side)

    def parse_uno(self):
        """<uno> -> '+' <uno> | '-' <uno> | <fator> ;"""
        if self.current_token[0] == token_map['+']['ADD']:
            op = self.current_token[1]
            self.consume(token_map['+']['ADD'])
            right_side = self.parse_uno() 
            return BinaryOpNode(LiteralNode("+", "operator"), op, right_side)
        elif self.current_token[0] == token_map['-']['SUB']:
            op = self.current_token[1]
            self.consume(token_map['-']['SUB'])
            right_side = self.parse_uno()
            return BinaryOpNode(LiteralNode("-", "operator"), op, right_side)
        else:
            return self.parse_fator()

    def parse_resto_mult(self, left_side):
        """
        <restoMult> -> '*' <uno> <restoMult>
                    | '/' <uno> <restoMult> 
                    | '%' <uno> <restoMult> | ε
        """
        if self.current_token[0] in [token_map['*']['MULT'], token_map['/']['DIV'], token_map['%']['MOD']]:
            op = self.current_token[1]
            self.consume(self.current_token[0])
            right_side = self.parse_uno()
            new_left = BinaryOpNode(left_side, op, right_side)
            return self.parse_resto_mult(new_left)
        return left_side

    def parse_ioStmt(self):
        """<ioStmt> -> 'system' '.' 'in' '.' 'scan'  '(' <type> ',' 'IDENT' ')' ';' 
        | 'system' '.' 'out' '.' 'print' '(' <outList> ')' ';' ;"""
        self.consume(token_map['system']['SYS'])
        self.consume(token_map['.']['PNT'])
        if self.current_token[0] == token_map['in']['IN']:
            self.consume(token_map['in']['IN'])
            self.consume(token_map['.']['PNT'])
            self.consume(token_map['scan']['SCAN'])
            self.consume(token_map['(']['LPAR'])
            type_node = self.parse_type()
            self.consume(token_map[',']['CLN'])
            ident = self.current_token[1]
            self.consume(token_map['IDEN'])
            node = IoNode("in", type_node, ident)
            self.consume(token_map[')']['RPAR'])
            self.consume(token_map[';']['SMCL'])
            return node
        if self.current_token[0] == token_map['out']['OUT']:
            self.consume(token_map['out']['OUT'])
            self.consume(token_map['.']['PNT'])
            self.consume(token_map['print']['PRT'])
            self.consume(token_map['(']['LPAR'])
            out_list = self.parse_outList()
            self.consume(token_map[')']['RPAR'])
            self.consume(token_map[';']['SMCL'])
            node = IoNode("out", out_list)
            return node
            
    def parse_outList(self):
        """<outList> -> <out> <restoOutList> ;"""
        out_item = self.parse_out()
        rest = self.parse_restoOutList()
        if rest is None:
            return out_item
        return [out_item] + rest
    
    def parse_out(self):
        """
        <out> -> 'STR' | 'IDENT' | 'NUMdec' | 'NUMfloat' | 'NUMoct' | 'NUMhex'
        """
        if self.current_token[0] == token_map['STR']:
            value = self.current_token[1]
            self.consume(token_map['STR'])
            return LiteralNode(value, 'string')
        elif self.current_token[0] == token_map['IDEN']:
            name = self.current_token[1]
            self.consume(token_map['IDEN'])
            return VariableNode(name)
        elif self.current_token[0] == token_map['INT']:
            value = self.current_token[1]
            self.consume(token_map['INT'])
            return LiteralNode(value, 'int')
        elif self.current_token[0] == token_map['FLT']:
            value = self.current_token[1]
            self.consume(token_map['FLT'])
            return LiteralNode(value, 'float')
        elif self.current_token[0] == token_map['OCT']:
            value = self.current_token[1]
            self.consume(token_map['OCT'])
            return LiteralNode(value, 'oct')
        elif self.current_token[0] == token_map['HEX']:
            value = self.current_token[1]
            self.consume(token_map['HEX'])
            return LiteralNode(value, 'hex')
        else:
            raise SyntaxError("Expressão de saída inválida.")

    def parse_restoOutList(self):
        """<restoOutList> -> ',' <out> <restoOutList> | ε"""
        if self.current_token[0] == token_map[',']['CLN']:
            self.consume(token_map[',']['CLN'])
            out_item = self.parse_out()
            rest = self.parse_restoOutList()
            if rest is None:
                return [out_item]
            return [out_item] + rest
        return None
            
            
    def parse_whileStmt(self):
        """<whileStmt> -> 'while' '(' <expr> ')' <stmt> ;"""
        self.consume(token_map['while']['WHL'])
        self.consume(token_map['(']['LPAR'])
        condition = self.parse_expr()
        self.consume(token_map[')']['RPAR'])
        body = self.parse_stmt()
        return WhileNode(condition, body)


    def parse_ifStmt(self):
        """<ifStmt> -> 'if' '(' <expr> ')' <stmt> <elsePart> ;"""
        self.consume(token_map['if']['IF'])
        self.consume(token_map['(']['LPAR'])
        condition = self.parse_expr()
        self.consume(token_map[')']['RPAR'])
        then_stmt = self.parse_stmt()
        else_stmt = self.parse_elsePart()
        node = IfNode(condition, then_stmt, else_stmt)
        return node
        
    def parse_elsePart(self):
        """<elsePart> -> 'else' <stmt> | & ;"""
        if self.current_token[0] == token_map['else']['ELSE']:
            self.consume(token_map['else']['ELSE'])
            return self.parse_stmt()
        return None
        
    def parse_fator(self):
        """
        <fator> -> 'NUMint' | 'NUMfloat' | 'NUMoct' | 'NUMhex'
                | 'IDENT'  | '(' <expr> ')' | 'STR'
        """
        if self.current_token[0] == token_map['INT']:
            value = self.current_token[1]
            self.consume(token_map['INT'])
            return LiteralNode(value, 'int')
        elif self.current_token[0] == token_map['FLT']:
            value = self.current_token[1]
            self.consume(token_map['FLT'])
            return LiteralNode(value, 'float')
        elif self.current_token[0] == token_map['OCT']:
            value = self.current_token[1]
            self.consume(token_map['OCT'])
            return LiteralNode(value, 'oct')
        elif self.current_token[0] == token_map['HEX']:
            value = self.current_token[1]
            self.consume(token_map['HEX'])
            return LiteralNode(value, 'hex')
        elif self.current_token[0] == token_map['IDEN']:
            name = self.current_token[1]
            self.consume(token_map['IDEN'])
            return VariableNode(name)
        elif self.current_token[0] == token_map['(']['LPAR']:
            self.consume(token_map['(']['LPAR'])
            expr = self.parse_expr()
            self.consume(token_map[')']['RPAR'])
            return expr
        elif self.current_token[0] == token_map['STR']:
            value = self.current_token[1]
            self.consume(token_map['STR'])
            return LiteralNode(value, 'string')

    def parse_declaration(self):
        """<declaration> -> <type> <identList> ';'"""
        variable_type = self.parse_type()
        ident_list = self.parse_identList()
        self.consume(token_map[';']['SMCL'])
        node = declarationNode(variable_type, ident_list)
        return node

    def parse_identList(self):
        """<identList> -> 'IDENT' <restoIdentList>"""
        ident = self.current_token[1]
        self.consume(token_map['IDEN'])
        rest = self.parse_restoIdentList()
        if rest is None:
            return [VariableNode(ident)]
        return [VariableNode(ident)] + rest

    def parse_restoIdentList(self):
        """<restoIdentList> -> ',' 'IDENT' <restoIdentList> | ε"""
        if self.current_token[0] == token_map[',']['CLN']:
            self.consume(token_map[',']['CLN'])
            ident = self.current_token[1]
            self.consume(token_map['IDEN'])
            rest = self.parse_restoIdentList()
            if rest is None:
                return [VariableNode(ident)]
            return [VariableNode(ident)] + rest
        return None