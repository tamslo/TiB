import os
import re
import time
import datetime

amino_map = {
    'ALA': 'A',
    'ARG': 'R',
    'ASN': 'N',
    'ASP': 'D',
    'CYS': 'C',
    'GLN': 'Q',
    'GLU': 'E',
    'GLY': 'G',
    'HIS': 'H',
    'ILE': 'I',
    'LEU': 'L',
    'LYS': 'K',
    'MET': 'M',
    'PHE': 'F',
    'PRO': 'P',
    'PYL': 'O',
    'SER': 'S',
    'SEC': 'U',
    'THR': 'T',
    'TRP': 'W',
    'TYR': 'Y',
    'VAL': 'V',
    'ASX': 'B',
    'GLX': 'Z',
    'XAA': 'X',
    'XLE': 'J'
}

id_map = {
    'T0761-D1': '4PW1|D1',
    'T0765-D1': '4PWU|D1',
    'T0774-D1': '4QB7|D1',
    'T0781-D2': '4QAN|D2'
}

def spaces_to_tabs(line):
    return re.sub(' +', '\t', line)

def get_output_path(output_directory, casp_id, with_timestamp):
    directory = output_directory + '/'
    if with_timestamp:
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S')
        timestamp += '_'
    else:
        timestamp = ''
    filename = timestamp + casp_id + '.fasta.txt'
    return directory + filename

def get_output_file(casp_id):
    output_directory = 'fasta'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_path = get_output_path(output_directory, casp_id, with_timestamp = False)
    return open(output_path, 'w')

def pdb_to_fasta(input_file):
    input_directory = 'pdb/'
    input = open(input_directory + input_file)
    casp_id = input_file.split('.pdb')[0]
    output = get_output_file(casp_id)
    # single line description
    output.write('>PDBID:' + id_map[casp_id] + '|CASP-ID:' + casp_id + '\n')
    line_length = 0
    
    for line in input:
        
        if line.startswith('ATOM'):
            line = spaces_to_tabs(line)
            fields = line.split('\t')
            
            if fields[2] == 'CA':
                
                 # it is  recommended that all lines of text be
                 # shorter than 80 characters
                if line_length == 80:
                    output.write('\n')
                    line_length = 0
                    
                output.write(amino_map[fields[3]])
                line_length += 1

    input.close()
    
    output_path = output.name
    output.close()
    validate_fasta(output_path, casp_id)

def get_sequence_from_fasta(fasta):
    sequence = ''
    for line in fasta:
        if line.startswith('>'):
            continue
        
        sequence += re.sub('\n', '', line)
    return sequence
            

def validate_fasta(generated_fasta_path, casp_id):
    plain_casp_id = casp_id.split('-D')[0]
    actual_fasta_path = 'fasta/' + plain_casp_id + '.fasta.txt'
    actual_fasta = open(actual_fasta_path, 'r')
    actual_sequence = get_sequence_from_fasta(actual_fasta)
    actual_fasta.close()

    generated_fasta = open(generated_fasta_path, 'r')
    generated_sequence = get_sequence_from_fasta(generated_fasta)
    generated_fasta.close()
    
    try:
        first_amino = actual_sequence.index(generated_sequence)
        status = 'VALID'
        position = str(first_amino + 1) + '-' + str(first_amino + len(generated_sequence))
        print(casp_id + '.pdb is ' + status + ', position of domain: ' + position)
    except ValueError:
        status = 'INVALID'
        print(casp_id + '.pdb is ' + status)
        

input_files = [
    'T0761-D1.pdb',
    'T0765-D1.pdb',
    'T0774-D1.pdb',
    'T0781-D2.pdb'
]
for input_file in input_files:
    pdb_to_fasta(input_file)
