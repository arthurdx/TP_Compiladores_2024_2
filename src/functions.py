from utils import token_map

def read_java_file(filename):
    with open(filename, 'r') as file:
        output = ""

        for line in file:
            current_row = 0
            current_word = ""
            #iterando sob linha e coluna no arquivo de texto
            while current_row < len(line):
                ch = line[current_row]

                if ch.isalpha():  # Permite letras, números e pontos
                    current_word += ch
                elif ch.isnumeric():
                    if current_word:
                        current_word+=ch
                    else:
                        pass
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
                    if current_word: # Processa a palavra antes de um símbolo
                        process_token(current_word, output)
                        current_word = ""
                    # Processa o símbolo individual
                    process_token(ch, output)

                current_row += 1

            # Processa a última palavra na linha, se existir
            if current_word:
                process_token(current_word, output)

        write_output_file("output.txt", output)

def process_token(word, output):
    # Verifica se a palavra está no token_map
    if word in token_map:
        token = token_map[word]
        print(f"{token}: '{word}'")
        output += f"{token}: '{word}'\n"
    # Se não for um token
    elif word.isidentifier():  
        print(f"IDEN: '{word}'")
        output += f"IDEN: '{word}'\n"
    elif word.startswith('"') and word.endswith('"'):
        print(f"STR: {word}") 
        output += f"STR: {word}\n"

def write_output_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def identify_loop(ch):
    return not ch.isnumeric()
