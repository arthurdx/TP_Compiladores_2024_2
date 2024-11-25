token_list = []
list_pos = 0

def current_token(token_list, list_pos):
    return token_list[list_pos] if list_pos < len(token_list) else None

def next_token(token_list, list_pos):
    if list_pos < len(token_list):
        list_pos += 1

def match(expected_token, token_list, list_pos):
    token = current_token(token_list, list_pos)
    assert token and token[0] == expected_token, f"Esperava {expected_token} but got {token[1]}" # Encontrar uma forma de mostrar o lexema no expected token
    next_token(token_list, list_pos)
    return token

#funções para processar os não terminais

def derive_type(token_list, list_pos):
    """<type> -> 'int' | 'float' | 'string'"""
    token = current_token(token_list, list_pos)
    assert token and token[0] in [20, 21, 22], f"Esperava as palavras reservadas['int', 'float', 'string'] mas encontrou {token[1]}"
    return match(token[0], token_list, list_pos)