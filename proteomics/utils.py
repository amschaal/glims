from tempfile import NamedTemporaryFile

def create_reverse(fasta_file):
    temp = NamedTemporaryFile(delete=True)
#     with open(fasta_file.path, 'r') as in_file:
    sequence = ''
    head = None
    for line in fasta_file:
        if line != '\n': # skip empty lines
            if line.startswith('>'):
                if head and sequence:
                    temp.write(head + '\n')
                    temp.write(sequence[::-1] + '\n')
                    sequence = ''
                head = line.strip()
            else:
                sequence += line.strip()
    fasta_file.seek(0)
    temp.write(head + '\n')
    temp.write(sequence[::-1] +  '\n')
    temp.seek(0)
    return temp

def concatenate_files(files=[]):
    temp = NamedTemporaryFile(delete=True)
    for file in files:
        file.seek(0)
        for line in file:
            temp.write(line)
    temp.seek(0)
    return temp
    
                    
def count_sequences(fasta_file):
    count = 0
    print fasta_file
    print fasta_file.file
    with open(fasta_file.file.path, 'r') as in_file:
        for line in in_file:
            if line.startswith('>'):
                count += 1
    return count
