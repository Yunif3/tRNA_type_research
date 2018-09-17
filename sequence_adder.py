#fixme delete this file later

def add_sequences(sequence_list1, sequence_list2):
    new_list = []
    for index, sequence1 in enumerate(sequence_list1):
        if sequence1[0:1] == '>':
            new_list.append(sequence1)
        else:
            new_line = ''
            new_line += sequence1.replace('\n', '')
            new_line += sequence_list2[index].replace('\n', '')
            new_line += '\n'
            new_list.append(new_line)
    return new_list


file1 = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the input file 1.\n')
file2 = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the input file 2.\n')
outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the output file.\n')

list1 = []
list2 = []
with open(file1, 'r') as input1:
    for line in input1:
        list1.append(line)

with open(file2, 'r') as input2:
    for line in input2:
        list2.append(line)

with open(outputFile, 'w') as output:
    result = add_sequences(list1, list2)
    for line in result:
        output.write(line)
