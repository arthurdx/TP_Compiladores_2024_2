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
        raise SyntaxError(f"Erro: Esperava '{expected_token}' ({get_token_name(expected_token)}), mas encontrou '{token[1] if token else None}'")
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
        raise SyntaxError(f"Erro: '=' esperado, mas encontrou '{current_token(token_list)[1] if current_token(token_list) else None}'")
    match(15, token_list)
    parse_expression(token_list)

def parse_expression(token_list):
    """<expression> -> <term> { ('+' | '-') <term> }"""
    parse_term(token_list)
    while current_token(token_list) and current_token(token_list)[0] in [1, 2]:  # '+' (ADD) e '-' (SUB)
        match(current_token(token_list)[0], token_list)
        parse_term(token_list)

def parse_term(token_list):
    """<term> -> <factor> { ('*' | '/' | '%') <factor> }"""
    parse_factor(token_list)
    while current_token(token_list) and current_token(token_list)[0] in [3, 4, 5]:  # '*', '/', '%'
        match(current_token(token_list)[0], token_list)
        parse_factor(token_list)

def parse_factor(token_list):
    """<factor> -> <identifier> | <number> | '(' <expression> ')'"""
    token = current_token(token_list)
    if not token:
        raise SyntaxError("Erro: Fator esperado, mas nenhum token encontrado")
    if token[0] == 47:  # IDEN
        match(47, token_list)
    elif token[0] in [43, 44, 45, 46]:  # Tipos de números (INT, OCT, HEX, FLT)
        match(token[0], token_list)
    elif token[0] == 39:  # '(' (LPAR)
        match(39, token_list)
        parse_expression(token_list)
        if not current_token(token_list) or current_token(token_list)[0] != 40:  # ')' (RPAR)
            raise SyntaxError(f"Erro: ')' esperado, mas encontrou '{current_token(token_list)[1] if current_token(token_list) else None}'")
        match(40, token_list)
    else:
        raise SyntaxError(f"Erro: Fator inválido encontrado '{token[1]}'")

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
    elif token[0] == 33:  # Código para 'break'
        parse_break_stmt(token_list)
    elif token[0] == 34:  # Código para 'continue'
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
    if current_token(token_list) and current_token(token_list)[0] == 14:  # 'else'
        match(14, token_list)
        parse_statement(token_list)  # Bloco de código após o else

def parse_break_stmt(token_list):
    """<breakStmt> -> 'break'"""
    match(33, token_list)  # 'break'

def parse_continue_stmt(token_list):
    """<continueStmt> -> 'continue'"""
    match(34, token_list)  # 'continue'

def parse_program(token_list):
    """<program> -> { <statement> ';' }"""
    global list_pos
    list_pos = 0  # Reinicia a posição para cada novo programa analisado
    while current_token(token_list):
        parse_statement(token_list)
        if not current_token(token_list) or current_token(token_list)[0] != 35:  # ';' (SMCL)
            raise SyntaxError(f"Erro: ';' esperado, mas encontrou '{current_token(token_list)[1] if current_token(token_list) else None}'")
        match(35, token_list)
