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
                        # current_word += '"'
                        process_token(current_word, output, current_line, current_row)
                        current_word = ""
                    elif ch == '/' and current_word == '/':
                        break
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

def process_token(word, output, current_line, current_row):
    try:
        token = identify_number(word) if word not in token_map else list(token_map[word].values())[0]

        if token:
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
        elif word.startswith('"') and word.endswith('"'):
                print(f"STR: {word}")
                output_line = ('STR', word, current_line, current_row - len(word))
                output.append(output_line)
        else:
            raise ValueError(f"String não fechada na linha: {current_line}")
    except ValueError as e:
        print(e)

def identify_number(word):
    assert not '..' in word or word.count('.') < 1 or not word.endswith('.'), f"Erro no número de ponto flutuante: '{word}' tem formato inválido."

    if word.isdigit():
        return 'INT'
    elif word.startswith('0') and all('0' <= ch <= '7' for ch in word[1:]):
        return 'OCT'
    elif word.startswith(('0x')) and all(ch.isdigit() or 'A' <= ch <= 'F' for ch in word[2:]):
        return 'HEX'
    elif '.' in word:
        before_point, after_point = word.split('.', 1)
        if before_point.isdigit() and (after_point.isdigit() or after_point == ""):
            assert after_point, f"Erro no número de ponto flutuante: '{word}' tem formato inválido."
            return 'FLT'
    return None

def identify_symbol(line, start):
    symbols = sorted(token_map.keys(), key=len, reverse=True)
    for symbol in symbols:
        if line.startswith(symbol, start):
            return symbol
    return None

def write_output_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
