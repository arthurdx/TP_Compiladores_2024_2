def read_java_file(filename):
    with open(filename, 'r') as file:
        current_line = 0
        current_row = 0
        #iterando sob linha e coluna no arquivo de texto
        for line in file:
            current_line += 1
            for ch in line:
                current_row += 1
                print(ch)



def write_output_file(filename, content):
    with open (filename, 'w') as file:
        file.write(content)