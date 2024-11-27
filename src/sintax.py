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
        raise SyntaxError(f"Erro: Esperava '{expected_token}', mas encontrou '{token[1] if token else None}'")
    next_token()
    return token

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
    if not token or token[0] != 10:
        raise SyntaxError(f"Erro: Identificador esperado, mas encontrou '{token[1] if token else None}'")
    match(10, token_list)

def parse_assignment(token_list):
    """<assignment> -> <identifier> '=' <expression>"""
    token = current_token(token_list)
    if not token or token[0] != 10:
        raise SyntaxError(f"Erro: Identificador esperado, mas encontrou '{token[1] if token else None}'")
    match(10, token_list)
    if not current_token(token_list) or current_token(token_list)[0] != 30:
        raise SyntaxError(f"Erro: '=' esperado, mas encontrou '{current_token(token_list)[1] if current_token(token_list) else None}'")
    match(30, token_list)
    parse_expression(token_list)

def parse_expression(token_list):
    """<expression> -> <term> { ('+' | '-') <term> }"""
    parse_term(token_list)
    while current_token(token_list) and current_token(token_list)[0] in [40, 41]:
        match(current_token(token_list)[0], token_list)
        parse_term(token_list)

def parse_term(token_list):
    """<term> -> <factor> { ('*' | '/') <factor> }"""
    parse_factor(token_list)
    while current_token(token_list) and current_token(token_list)[0] in [42, 43]:
        match(current_token(token_list)[0], token_list)
        parse_factor(token_list)

def parse_factor(token_list):
    """<factor> -> <identifier> | <number> | '(' <expression> ')'"""
    token = current_token(token_list)
    if not token:
        raise SyntaxError("Erro: Fator esperado, mas nenhum token encontrado")
    if token[0] == 10:
        match(10, token_list)
    elif token[0] in [50, 51]:
        match(token[0], token_list)
    elif token[0] == 60:
        match(60, token_list)
        parse_expression(token_list)
        if not current_token(token_list) or current_token(token_list)[0] != 61:
            raise SyntaxError(f"Erro: ')' esperado, mas encontrou '{current_token(token_list)[1] if current_token(token_list) else None}'")
        match(61, token_list)
    else:
        raise SyntaxError(f"Erro: Fator inválido encontrado '{token[1]}'")

def parse_statement(token_list):
    """<statement> -> <declaration> | <assignment>"""
    token = current_token(token_list)
    if not token:
        raise SyntaxError("Erro: Declaração ou atribuição esperada, mas nenhum token encontrado")
    if token[0] in [20, 21, 22]:
        parse_declaration(token_list)
    elif token[0] == 10:
        parse_assignment(token_list)
    else:
        raise SyntaxError(f"Erro: Declaração ou atribuição inválida encontrada '{token[1]}'")

def parse_program(token_list):
    """<program> -> { <statement> ';' }"""
    global list_pos
    list_pos = 0  # Reinicia a posição para cada novo programa analisado
    while current_token(token_list):
        parse_statement(token_list)
        if not current_token(token_list) or current_token(token_list)[0] != 70:
            raise SyntaxError(f"Erro: ';' esperado, mas encontrou '{current_token(token_list)[1] if current_token(token_list) else None}'")
        match(70, token_list)
