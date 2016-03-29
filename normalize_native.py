import os

def get_residue(line):
    column = 25
    residue = ''
    while (True):
        if line[column] != ' ':
            residue += line[column]
            column -= 1
        else:
            break
    return residue

def spaces(number):
    spaces = ''
    spaces += ' ' * number
    return spaces

def change_residue(line, line_number):
    column = 25
    deletions = 0
    while (True):
        if line[column] != ' ':
            line = line[:column] + line[column + 1:]
            column -= 1
            deletions += 1
        else:
            break
    line_number = str(line_number)
    pre_spaces = spaces(deletions - len(line_number))
    return line[:column] + pre_spaces + line_number + line[column + 1:]

def normalize_native(file_name):
    file_path = 'pdb/' + file_name
    original = open(file_path, 'r')
    split_path = file_path.split('.pdb')
    normalized_path = split_path[0] + '_normalized.pdb'
    normalized = open(normalized_path, 'w')

    residue = 1
    previous_residue = ''

    for line in original:
        if line.startswith('ATOM'):
            current_residue = get_residue(line)
            if previous_residue != '' and current_residue != previous_residue:
                residue += 1
            line = change_residue(line, residue)
            previous_residue = current_residue

        normalized.write(line)

    original.close()
    normalized.close()

    # os.remove(file_path)
    # os.rename(normalized_path, file_path)

input_files = [
    'T0761-D1.pdb',
    'T0765-D1.pdb',
    'T0781-D2.pdb'
]
for input_file in input_files:
    normalize_native(input_file)
