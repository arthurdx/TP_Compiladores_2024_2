from utils import *

class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.pos = 0
        self.current_token = None

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
        print(f"Token consumido: {self.current_token[1]}")
        self.next_position()

    def parse_function(self):
        """<function*> -> <type> 'IDENT' '(' ')' <bloco>'"""
        self.set_current_token()
        self.parse_type()
        self.consume(token_map['IDEN'])
        self.consume(token_map['(']['LPAR'])
        self.consume(token_map[')']['RPAR'])
        self.parse_bloco()
        if self.pos < len(self.token_list):
            raise SyntaxError(f"Token inesperado '{self.current_token[1] if self.current_token else None}', "
                              f"na linha '{self.current_token[2] if self.current_token else None}' e "
                              f"na coluna '{self.current_token[3] if self.current_token else None}'. Esperado: fim do arquivo.")

    def parse_type(self):
        """<type> -> 'int' | 'float' | 'string'"""
        if self.current_token[0] == token_map['int']['KINT']:
            self.consume(token_map['int']['KINT'])
        elif self.current_token[0] == token_map['float']['KFLT']:
            self.consume(token_map['float']['KFLT'])
        elif self.current_token[0] == token_map['string']['KSTR']:    
            self.consume(token_map['string']['KSTR'])
        

    
    def parse_bloco(self):
        """<bloco> -> '{' <stmList> '}'"""
        self.consume(token_map['{']['LBRC'])
        self.parse_stmList()
        self.consume(token_map['}']['RBRC'])

    def parse_stmList(self):
        """<stmList> -> <stm> <stmList> | &"""
        if self.current_token and self.current_token[0] != token_map['}']['RBRC']:
            self.parse_stmt()
            self.parse_stmList()

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
            self.parse_forStmt()
        elif self.current_token[0] == token_map['system']['SYS']:
            self.parse_ioStmt()
        elif self.current_token[0] == token_map['while']['WHL']:
            self.parse_whileStmt()
        elif self.current_token[0] == token_map['IDEN']:
            self.parse_atrib()
            self.consume(token_map[';']['SMCL'])
        elif self.current_token[0] == token_map['if']['IF']:
            self.parse_ifStmt()
        elif self.current_token[0] == token_map['{']['LBRC']:
            self.parse_bloco()
        elif self.current_token[0] == token_map['break']['BRK']:
            self.consume(token_map['break']['BRK'])
        elif self.current_token[0] == token_map['continue']['CTN']:
            self.consume(token_map['continue']['CTN'])
        elif self.current_token[0] in [token_map['int']['KINT'], token_map['float']['KFLT'], token_map['string']['KSTR']]:
            self.parse_declaration()            
        elif self.current_token[0] == token_map[';']['SMCL']:
            self.consume(token_map[';']['SMCL'])
        elif self.current_token[0] == token_map['}']['RBRC']:
            self.consume(token_map['}']['RBRC'])
        
        

    def parse_forStmt(self):
        """<forStmt> -> 'for' '(' <optAtrib> ';' <optExpr> ';' <optAtrib> ')' <stmt> ;r"""
        self.consume(token_map['for']['FOR'])
        self.consume(token_map['(']['LPAR'])
        self.parse_optAtrib()
        self.consume(token_map[';']['SMCL'])
        self.parse_optExpr()
        self.consume(token_map[';']['SMCL'])
        self.parse_optAtrib()
        self.consume(token_map[')']['RPAR'])
        self.parse_stmt()

    def parse_optAtrib(self):
        """<optAtrib> -> <atrib> | & ;"""
        if self.current_token[0] == token_map['IDEN']:
            self.parse_atrib()

    def parse_atrib(self):
        """
        <atrib> -> 'IDENT' '=' <expr> 
         | 'IDENT' '+=' <expr> 
         | 'IDENT' '-=' <expr> 
         | 'IDENT' '*=' <expr> 
         | 'IDENT' '/=' <expr> 
         | 'IDENT' '%=' <expr>;
        """
        self.consume(token_map['IDEN'])
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
        self.parse_expr()

    def parse_optExpr(self):
        """<optExpr> -> <expr> | & """
        if self.current_token[0] != token_map[';']['SMCL']:
            self.parse_expr()
                    

    def parse_expr(self):
        "<expr> -> <or> ;"
        self.parse_or()

    def parse_or(self):
        """<or> -> <and> <restoOr> ;"""
        self.parse_and()
        self.parse_resto_or()

    def parse_resto_or(self):
        """<restoOr> -> '||' <and> <restoOr> | & ;"""
        if self.current_token[0] == token_map['||']['OR']:
            self.consume(token_map['||']['OR'])
            self.parse_and()    
            self.parse_resto_or()    

    def parse_and(self):
        """<and> -> <not> <restoAnd> ;"""
        self.parse_not()
        self.parse_resto_and()

    def parse_resto_and(self):
        """<restoAnd> -> '&&' <not> <restoAnd> | & ;"""
        if self.current_token[0] == token_map['&&']['AND']:
            self.consume(token_map['&&']['AND'])
            self.parse_not()    
            self.parse_resto_and()

    def parse_not(self):
        """<not> -> '!' <not> | <rel> ;"""
        if self.current_token[0] == token_map['!']['NOT']:
            self.consume(token_map['!']['NOT'])
            self.parse_not()  
        else:  
            self.parse_rel()
        
    def parse_rel(self):
        """<rel> -> <add> <restoRel> ;"""
        self.parse_add()
        self.parse_resto_rel()

    def parse_resto_rel(self):
        """<restoRel> -> '==' <add> | '!=' <add>
            | '<' <add> | '<=' <add> 
            | '>' <add> | '>=' <add> | & ;
        """
        if self.current_token[0] == token_map['==']['EQL']:
            self.consume(token_map['==']['EQL'])
            self.parse_add()
        elif self.current_token[0] == token_map['!=']['DIF']:
            self.consume(token_map['!=']['DIF'])
            self.parse_add()
        elif self.current_token[0] == token_map['>']['GT']:
            self.consume(token_map['>']['GT'])
            self.parse_add()
        elif self.current_token[0] == token_map['>=']['GET']:
            self.consume(token_map['>=']['GET'])
            self.parse_add()
        elif self.current_token[0] == token_map['<']['LT']:
            self.consume(token_map['<']['LT'])
            self.parse_add()
        elif self.current_token[0] == token_map['<=']['LET']:
            self.consume(token_map['<=']['LET'])
            self.parse_add()

    def parse_add(self):
        """<add> -> <mult> <restoAdd> ;"""
        self.parse_mult()
        self.parse_resto_add()

    def parse_resto_add(self):
        """<restoAdd> -> '+' <mult> <restoAdd> 
            | '-' <mult> <restoAdd> | & ;""" 
        if self.current_token[0] == token_map['+']['ADD']:
            self.consume(token_map['+']['ADD'])
            self.parse_mult() 
            self.parse_resto_add()
        elif self.current_token[0] == token_map['-']['SUB']:
            self.consume(token_map['-']['SUB'])
            self.parse_mult()  
            self.parse_resto_add()

    def parse_mult(self):
        """<mult> -> <uno> <restoMult> ;"""
        self.parse_uno()
        self.parse_resto_mult()

    def parse_uno(self):
        """<uno> -> '+' <uno> | '-' <uno> | <fator> ;"""
        if self.current_token[0] == token_map['+']['ADD']:
            self.consume(token_map['+']['ADD'])
            self.parse_uno() 
        elif self.current_token[0] == token_map['-']['SUB']:
            self.consume(token_map['-']['SUB'])
            self.parse_uno()
        else:
            self.parse_fator()

    def parse_resto_mult(self):
        """<restoMult> -> '*' <uno> <restoMult>
            |  '/' <uno> <restoMult> 
            |  '%' <uno> <restoMult> | & ;
        """
        if self.current_token[0] == token_map['*']['MULT']:
            self.consume(token_map['*']['MULT'])
            self.parse_uno()
            self.parse_resto_mult()
        elif self.current_token[0] == token_map['/']['DIV']:
            self.consume(token_map['/']['DIV'])
            self.parse_uno()
            self.parse_resto_mult()
        elif self.current_token[0] == token_map['%']['MOD']:
            self.consume(token_map['%']['MOD'])
            self.parse_uno()
            self.parse_resto_mult()

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
            self.parse_type()
            self.consume(token_map[',']['CLN'])
            self.consume(token_map['IDEN'])
            self.consume(token_map[')']['RPAR'])
            self.consume(token_map[';']['SMCL'])
        if self.current_token[0] == token_map['out']['OUT']:
            self.consume(token_map['out']['OUT'])
            self.consume(token_map['.']['PNT'])
            self.consume(token_map['print']['PRT'])
            self.consume(token_map['(']['LPAR'])
            self.parse_outList()
            self.consume(token_map[')']['RPAR'])
            self.consume(token_map[';']['SMCL'])
            
    def parse_outList(self):
        """<outList> -> <out> <restoOutList> ;"""
        self.parse_out()
        self.parse_restoOutList()
    
    def parse_out(self):
        """<out> -> 'STR' | 'IDENT' | 'NUMdec' | 'NUMfloat' | 'NUMoct' | 'NUMhex'"""
        if self.current_token[0] == token_map['STR']:
            self.consume(token_map['STR'])
        if self.current_token[0] == token_map['IDEN']:
            self.consume(token_map['IDEN'])
        if self.current_token[0] == token_map['INT']:
            self.consume(token_map['INT'])
        if self.current_token[0] == token_map['FLT']:
            self.consume(token_map['FLT'])
        if self.current_token[0] == token_map['OCT']:
            self.consume(token_map['OCT'])
        if self.current_token[0] == token_map['HEX']:
            self.consume(token_map['HEX'])
        
    def parse_restoOutList(self):
        """<restoOutList> -> ',' <out> <restoOutList> | & ;"""
        if self.current_token[0] == token_map[',']['CLN']:
            self.consume(token_map[',']['CLN'])
            self.parse_out()
            self .parse_restoOutList()
            
            
    def parse_whileStmt(self):
        """<whileStmt> -> 'while' '(' <expr> ')' <stmt> ;"""
        self.consume(token_map['while']['WHL'])
        self.consume(token_map['(']['LPAR'])
        self.parse_expr()
        self.consume(token_map[')']['RPAR'])
        self.parse_stmt()


    def parse_ifStmt(self):
        """<ifStmt> -> 'if' '(' <expr> ')' <stmt> <elsePart> ;"""
        self.consume(token_map['if']['IF'])
        self.consume(token_map['(']['LPAR'])
        self.parse_expr()
        self.consume(token_map[')']['RPAR'])
        self.parse_stmt()
        self.parse_elsePart()
        
    def parse_elsePart(self):
        """<elsePart> -> 'else' <stmt> | & ;"""
        if self.current_token[0] == token_map['else']['ELSE']:
            self.consume(token_map['else']['ELSE'])
            parse_stmt()
        
    def parse_fator(self):
        """<fator> -> 'NUMint' | 'NUMfloat' | 'NUMoct' | 'NUMhex'
         | 'IDENT'  | '(' <expr> ')' | 'STR'"""

        if self.current_token[0] == token_map['INT']:
            self.consume(token_map['INT'])
        elif self.current_token[0] == token_map['FLT']:
            self.consume(token_map['FLT'])
        elif self.current_token[0] == token_map['OCT']:    
            self.consume(token_map['OCT'])
        elif self.current_token[0] == token_map['HEX']:
            self.consume(token_map['HEX'])
        elif self.current_token[0] == token_map['IDEN']:
            self.consume(token_map['IDEN'])
        elif self.current_token[0] == token_map['(']['LPAR']:
            self.consume(token_map['(']['LPAR'])
            self.parse_expr()
            self.consume(token_map[')']['RPAR'])
        elif self.current_token[0] == token_map['STR']:
            self.consume(token_map['STR'])

    
    def parse_declaration(self):
        """<declaration> -> <type> <identList> ';'"""
        self.parse_type()
        self.parse_identList()
        self.consume(token_map[';']['SMCL'])

    def parse_identList(self):
        """<identList> -> 'IDENT' <restoIdentList>"""
        self.consume(token_map['IDEN'])
        self.parse_restoIdentList()

    def parse_restoIdentList(self):
        """<restoIdentList> -> ',' 'IDENT' <restoIdentList> | & ;"""
        if self.current_token[0] == token_map[',']['CLN']:
            self.consume(token_map[',']['CLN'])
            self.consume(token_map['IDEN'])
            self.parse_restoIdentList()
    
    
