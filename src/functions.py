from utils import token_map

def read_java_file(filename):
    with open(filename, 'r') as file:
        current_line = 0
        current_row = 0
        output = ""
        #iterando sob linha e coluna no arquivo de texto
        current_word = ""
        for line in file:
            current_line += 1
            current_row = 0
            print(len(line))
            while current_row < len(line):
                ch = line[current_row]
                current_word += ch
                if identify_loop(ch):
                    current_row += 1
                    ch = line[current_row]
                    while ch.isalnum():
                        current_word += ch
                        current_row += 1
                        ch = line[current_row]
                        
                    print(current_word)
                        
                    
                        


                

                




def write_output_file(filename, content):
    with open (filename, 'w') as file:
        file.write(content)

def identify_loop(ch):
    if ch.isnumeric():
        return False
    
    return True
        