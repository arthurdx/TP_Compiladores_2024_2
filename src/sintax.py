from utils import token_map

list_pos = 0

def current_token(token_list):
    """Obtém o token atual."""
    global list_pos
    return token_list[list_pos] if list_pos < len(token_list) else None

def next_token():
    """Avança para o próximo token."""
    global list_pos
    list_pos += 1

def match(expected_token, token_list):
    """
    Verifica se o token atual corresponde ao esperado e avança.
    """
    token = current_token(token_list)
    if not token or token[0] != expected_token:
        raise SyntaxError(f"Erro: Esperava '{expected_token}' ({get_token_name(expected_token)}), mas encontrou '{token[1] if token else None}, na linha {token[2]} e na coluna {token[3]}.'")
    next_token()
    return token

def get_token_name(token_value):
    """Obtém o nome do token a partir do token_map."""
    for key, value in token_map.items():
        if isinstance(value, dict):
            for _, v in value.items():
                if v == token_value:
                    return key
    return "Desconhecido"

# Funções para derivar os não terminais da gramática

def parse_function(token_list):
    """<function*> -> <type> 'IDENT' '(' ')' <bloco>'"""
    parse_type(token_list)


def parse_type(token_list):
    """<type> -> 'int' | 'float' | 'string'"""
    token = current_token(token_list)
    if not token or token[0] not in [20, 21, 22]:
        raise SyntaxError(f"Erro: Tipo esperado ('int', 'float', 'string'), mas encontrou '{token[1] if token else None}'")
    match(token[0], token_list)

def parse_declaration(token_list):
    """<declaration> -> <type> <identifier>"""
    parse_type(token_list)
    token = current_token(token_list)
    if not token or token[0] != 47:  # 47 é o código de IDEN
        raise SyntaxError(f"Erro: Identificador esperado, mas encontrou '{token[1] if token else None}'")
    match(47, token_list)

def parse_assignment(token_list):
    """<assignment> -> <identifier> '=' <expression>"""
    token = current_token(token_list)
    if not token or token[0] != 47:  # 47 é o código de IDEN
        raise SyntaxError(f"Erro: Identificador esperado, mas encontrou '{token[1] if token else None}'")
    match(47, token_list)
    if not current_token(token_list) or current_token(token_list)[0] != 15:  # 15 é o código de ASSG ('=')
        raise SyntaxError(f"Erro: '=' esperado, mas encontrou '{current_token(token_list)[1] if current_token(token_list)[0](token_list) else None}'")
    match(15, token_list)
    parse_expression(token_list)

def parse_expression(token_list):
    """<expression> -> <or>"""
    parse_or(token_list)

def parse_or(token_list):
    """<or> -> <and> <restoOr>"""
    parse_and(token_list)
    parse_resto_or(token_list)

def parse_resto_or(token_list):
    """<restoOr> -> '||' <and> <restoOr> | & ;"""
    if current_token(token_list)[0] == token_map['||']['OR']:
        match(token_map['||']['OR'], token_list)
        parse_and(token_list)
        parse_resto_or(token_list)


def parse_and(token_list):
    """"<and> -> <not> <restoAnd> ;"""
    parse_not(token_list)
    parse_resto_and(token_list)

def parse_resto_and(token_list):
    """<restoAnd> -> '&&' <not> <restoAnd> | & ;"""
    parse_not(token_list)
    if current_token(token_list)[0] ==token_map['&&']['AND']:
        match(token_map['&&']['AND'], token_list)
        parse_not(token_list)
        parse_resto_and(token_list)

def parse_not(token_list):
    """<not> -> '!' <not> | <rel> ;"""
    if current_token(token_list)[0] == token_map['!']['NOT']:
        match (token_map['!']['NOT'], token_list)
        parse_not(token_list)
    else:
        parse_rel(token_list)

def parse_rel(token_list):
    """<rel> -> <add> <restoRel> ;"""
    parse_add(token_list)
    parse_resto_rel(token_list)

def parse_resto_rel(token_list):
    """
    <restoRel> -> '==' <add> | '!=' <add>
            | '<' <add> | '<=' <add> 
            | '>' <add> | '>=' <add> | & ;
    """
    if current_token(token_list)[0] == token_map['==']['EQL']:
        match (token_map['==']['EQL'])
        parse_add(token_list)
    elif current_token(token_list)[0] == token_map['!=']['DIF']:
        match (token_map['!=']['DIF'])
        parse_add(token_list)
    elif current_token(token_list)[0] == token_map['<']['LT']:
        match (token_map['<']['LT'])
        parse_add(token_list) 
    elif current_token(token_list)[0] == token_map['>']['GT']:
        match (token_map['>']['GT'])
        parse_add(token_list)
    elif current_token(token_list)[0] == token_map['<=']['LET']:
        match (token_map['<=']['LET'])
        parse_add(token_list) 
    elif current_token(token_list)[0] == token_map['>=']['GET']:
        match (token_map['>=']['GET'])
        parse_add(token_list)

def parse_add(token_list):
    """<add> -> <mult> <restoAdd> ;"""
    parse_mult(token_list)
    parse_resto_add(token_list)

def parse_resto_add(token_list):
    """
    <restoAdd> -> '+' <mult> <restoAdd> 
            | '-' <mult> <restoAdd> | & ;
    """
    if current_token(token_list)[0] == token_map['+']['ADD']:
        match (token_map['+']['ADD'])
        parse_resto_add(token_list)
    elif current_token(token_list)[0] == token_map['-']['SUB']:
        match (token_map['-']['SUB'])
        parse_resto_add(token_list) 

def parse_mult(token_list):
    """<mult> -> <uno> <restoMult> ;"""
    parse_uno(token_list)
    parse_resto_mult(token_list)

def parse_resto_mult(token_list):
    """
    <restoMult> -> '*' <uno> <restoMult>
            |  '/' <uno> <restoMult> 
            |  '%' <uno> <restoMult> | & ;
    """
    if current_token(token_list)[0] == token_map['*']['MULT']:
        match (token_map['*']['MULT'])
        parse_resto_mult(token_list)
    elif current_token(token_list)[0] == token_map['/']['DIV']:
        match (token_map['/']['DIV'])
        parse_resto_mult(token_list)
    elif current_token(token_list)[0] == token_map['%']['MOD']:
        match (token_map['%']['MOD'])
        parse_resto_mult(token_list)

def parse_uno(token_list):
    """<uno> -> '+' <uno> | '-' <uno> | <fator> ;"""
    if current_token(token_list)[0] == token_map['+']['ADD']:
        match (token_map['+']['ADD'], token_list)
        parse_uno(token_list)
    elif current_token(token_list)[0] == token_map['-']['SUB']:
        match (token_map['-']['SUB'], token_list)
        parse_uno(token_list)
    else:
        parse_fator(token_list)

def parse_fator(token_list):
    """
    <fator> -> 'NUMint' | 'NUMfloat' | 'NUMoct' | 'NUMhex'
         | 'IDENT'  | '(' <expr> ')' | 'STR';
    """
    if current_token(token_list)[0] == token_map['STR']:
        match (token_map['STR'], token_list)
    elif current_token(token_list)[0] == token_map['INT']:
        match (token_map['INT'], token_list)
    elif current_token(token_list)[0] == token_map['OCT']:
        match (token_map['OCT'], token_list)
    elif current_token(token_list)[0] == token_map['HEX']:
        match (token_map['HEX'], token_list)
    elif current_token(token_list)[0] == token_map['FLT']:
        match (token_map['FLT'], token_list)
    elif current_token(token_list)[0] == token_map['IDEN']:
        match (token_map['IDEN'], token_list)    
    else:
        parse_expression(token_list)


def parse_statement(token_list):
    """<statement> -> <declaration> | <assignment> | <ifStmt>"""
    token = current_token(token_list)
    if not token:
        raise SyntaxError("Erro: Declaração ou atribuição ou if esperado, mas nenhum token encontrado")
    
    if token[0] in [20, 21, 22]:  # 'int', 'float', 'string'
        parse_declaration(token_list)
    elif token[0] == 47:  # IDEN
        parse_assignment(token_list)
    elif token[0] == 27:  # 'if'
        parse_if_stmt(token_list)
    elif token[0] == 33:  
        parse_break_stmt(token_list)
    elif token[0] == 34:
        parse_continue_stmt(token_list)
    else:
        raise SyntaxError(f"Erro: Comando inválido encontrado '{token[1]}'")

def parse_if_stmt(token_list):
    """<ifStmt> -> 'if' '(' <expression> ')' <stmt> <elsePart>"""
    match(27, token_list)  # 'if'
    match(39, token_list)  # '('
    parse_expression(token_list)  # Expressão do if
    match(40, token_list)  # ')'
    
    # Bloco de código após o if
    parse_statement(token_list) 
    
    # Parte else
    if current_token(token_list)[0](token_list) and current_token(token_list)[0] == 14: 
        match(14, token_list)
        parse_statement(token_list) 

def parse_break_stmt(token_list):
    """<breakStmt> -> 'break'"""
    match(33, token_list)  

def parse_continue_stmt(token_list):
    """<continueStmt> -> 'continue'"""
    match(34, token_list) 

def parse_program(token_list):
    """<program> -> { <statement> ';' }"""
    global list_pos
    list_pos = 0  
    while current_token(token_list):
        parse_statement(token_list)
        if not current_token(token_list) or current_token(token_list)[0] != 35:  # ';' (SMCL)
            raise SyntaxError(f"Erro: ';' esperado, mas encontrou '{current_token(token_list)[1] if current_token(token_list)[0](token_list) else None}, na linha {current_token(token_list)[2]} e na coluna {current_token(token_list)[3]}'")
        match(35, token_list)
