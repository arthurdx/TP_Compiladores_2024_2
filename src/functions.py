from utils import token_map  # Importa o mapa de tokens

def read_java_file(filename):
    with open(filename, 'r') as file:
        output = []
        current_line = 0
        reading_comment = False
        for line in file:
            if line == '\n':
                line.replace('\n', '\\n')
            current_row = 0
            current_word = ""
            negative_sign = False

            if not reading_comment:
                while current_row < len(line):
                    ch = line[current_row]

                    if ch == '/' and current_row + 1 < len(line) and line[current_row + 1] == '/':
                        break

                    elif ch == '/' and current_row + 1 < len(line) and line[current_row + 1] == '*':
                        comment_start_line = current_line
                        reading_comment = True
                        break

                    if ch.isalpha(): 
                        current_word += ch
                    elif ch.isdigit() or (ch == '.' and current_word and current_word[-1].isdigit()):  
                        current_word += ch
                    elif ch == 'x' and current_word == '0': 
                        current_word += ch
                    elif ch == '"':  
                        if current_word:
                            process_token(current_word, output, current_line, current_row)
                            current_word = ""
                        current_word += ch
                        current_row += 1
                        while current_row < len(line) and line[current_row] != '"':
                            current_word += line[current_row]
                            current_row += 1
                        current_word += '"'
                        process_token(current_word, output, current_line, current_row)
                        current_word = ""
                    elif ch == '/' and current_word == '/':
                        break
                    elif ch == '-':
                        if current_row + 1 < len(line) and (line[current_row + 1].isdigit() or line[current_row + 1] == '.'):
                            negative_sign = True
                        else:
                            if current_word:
                                process_token(current_word, output, current_line, current_row)
                                current_word = ""
                            symbol_token = identify_symbol(line, current_row)
                            if symbol_token:
                                process_token(symbol_token, output, current_line, current_row)
                                current_row += len(symbol_token) - 1


                    else:
                        if current_word:  
                            process_token(current_word, output, current_line, current_row)
                            current_word = ""

                        symbol_token = identify_symbol(line, current_row)
                        if symbol_token:
                            process_token(symbol_token, output, current_line, current_row)
                            current_row += len(symbol_token) - 1  

                    current_row += 1

                current_line += 1
                if current_word:
                    process_token(current_word, output, current_line, current_row)
            else:
                while '*/' not in line:
                    assert len(line) > 1, f'Bloco de comentário não fechado, linha: {comment_start_line + 1}' 
                    current_line += 1
                    break
                else:
                    reading_comment = False   
            
        
        return output

        #write_output_file("output.txt", output)

def process_token(word, output, current_line ,current_row):
    token, error_message = identify_number(word) if word not in token_map else (list(token_map[word].values())[0], None)
    
    if error_message:
        print(error_message)
    elif token:
        if token == 'FLT' and not word.endswith('.'):
            word += '0'
        print(f"{token}: '{word}'")
        output_line = (token, word, current_line, current_row - len(word))
        output.append(output_line)
    elif word in token_map:
        token = list(token_map[word].keys())[0]
        print(f"{token}: '{word}'")
        output_line = (token, word, current_line, current_row - len(word))
        output.append(output_line)
    elif word.isidentifier():
        print(f"IDEN: '{word}'")
        output_line = ('IDEN', word, current_line, current_row - len(word))
        output.append(output_line)
    elif word.startswith('"'):
        if word.endswith('"'):
            print(f"STR: {word}") 
            output_line = ('STR', word, current_line, current_row - len(word))
            output.append(output_line)
        else:
            raise ValueError(f"String not closed: {word}")

def identify_number(word):
    errors = []

    if '..' in word:
        errors.append(f"Erro: número '{word}' não pode conter dois ou mais pontos consecutivos.")

    if word.count('.') > 1:
        errors.append(f"Erro: número '{word}' não pode ter mais de um ponto.")

    if word.endswith('.') and len(word) > 1:
        errors.append(f"Erro: número '{word}' não pode terminar com um ponto sem dígitos.")

    if errors:
        return None, " | ".join(errors)

    if word[0] == '-':
        number_part = word[1:] 
    else:
        number_part = word
        
    if word[0] in '123456789' and word.isdigit():
        return 'INT', None
    
    elif word.startswith('0') and all('0' <= ch <= '7' for ch in word[1:]):
        return 'OCT', None
    
    elif word.startswith(('0x')) and all(ch.isdigit() or 'A' <= ch <= 'F' for ch in word[2:]):
        return 'HEX', None
    
    elif '.' in word:
        before_point, after_point = word.split('.', 1)
        if before_point.isdigit() and (after_point.isdigit() or after_point == ""):
            return 'FLT', None
    
    return None, None

def identify_symbol(line, start):
    symbols = sorted(token_map.keys(), key=len, reverse=True)
    for symbol in symbols:
        if line.startswith(symbol, start):
            return symbol
    return None

def write_output_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
