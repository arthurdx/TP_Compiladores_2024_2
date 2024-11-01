from utils import token_map  # Importa o mapa de tokens

def read_java_file(filename):
    with open(filename, 'r') as file:
        output = ""
        
        for line in file:
            current_row = 0
            current_word = ""
            
            while current_row < len(line):
                ch = line[current_row]

                if ch.isalpha(): 
                    current_word += ch
                elif ch.isdigit() or (ch == '.' and current_word and current_word[-1].isdigit()):  
                    current_word += ch
                elif ch == 'x' and current_word == '0': 
                    current_word += ch
                elif ch == '"':  
                    if current_word:
                        process_token(current_word, output)
                        current_word = ""
                    current_word += ch
                    current_row += 1
                    while current_row < len(line) and line[current_row] != '"':
                        current_word += line[current_row]
                        current_row += 1
                    current_word += '"'
                    process_token(current_word, output)
                    current_word = ""
                else:
                    if current_word:  
                        process_token(current_word, output)
                        current_word = ""

                    symbol_token = identify_symbol(line, current_row)
                    if symbol_token:
                        process_token(symbol_token, output)
                        current_row += len(symbol_token) - 1  

                current_row += 1

            if current_word:
                process_token(current_word, output)

        write_output_file("output.txt", output)

def process_token(word, output):
    token = identify_number(word) if word not in token_map else list(token_map[word].keys())[0]
    
    if token:
        print(f"{token}: '{word}'")
        output += f"{token}: '{word}'\n"
    elif word in token_map:
        token = list(token_map[word].keys())[0]
        print(f"{token}: '{word}'")
        output += f"{token}: '{word}'\n"
    elif word.isidentifier():
        print(f"IDEN: '{word}'")
        output += f"IDEN: '{word}'\n"
    elif word.startswith('"') and word.endswith('"'):
        print(f"STR: {word}") 
        output += f"STR: {word}\n"

def identify_number(word):
    if word[0] in '123456789' and word.isdigit():
        return 'DEC'
    
    elif word.startswith('0') and all('0' <= ch <= '7' for ch in word[1:]):
        return 'OCT'
    
    elif word.startswith(('0x', '0X')) and all(ch.isdigit() or 'A' <= ch <= 'F' or 'a' <= ch <= 'f' for ch in word[2:]):
        return 'HEX'
    
    elif '.' in word:
        before_point, after_point = word.split('.', 1)
        if before_point.isdigit() and (after_point.isdigit() or after_point == ""):
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
