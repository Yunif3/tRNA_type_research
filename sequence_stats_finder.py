def write_sorted_lengths_file(file):
    file.write('<SORTED LENGTHS>\n')
    for length in sequence_length_options:
        file.write('tRNAs with {0:d} bases in V-loop.\n'.format(length))
        file.write(
            'There are {0:d} cases out of {1:d} sequences.\n'.format(len(length_group_dic[length]), len(sequences)))
        for loc in length_group_dic[length]:
            file.write(str(labels[loc]) + '\n')
            file.write(str(sequences[loc]) + '\n')


def write_selected_length_file(file, length):
    for index in length_group_dic[length]:
        file.write('>' + str(index) + '\n')
        file.write(sequences[index] + '\n')


def find_base_proportion(length):
    result = ''
    for base_position in range(length):
        base_counts = [0] * 4
        base_percentage = [0] * 4
        for sequence_location in length_group_dic[length]:
            base = sequences[sequence_location][base_position]
            if base == 'A':
                base_counts[0] += 1
            elif base == 'T' or base == 'U':
                base_counts[1] += 1
            elif base == 'C':
                base_counts[2] += 1
            elif base == 'G':
                base_counts[3] += 1
            else:
                result += '{} contains INVALID base.\n'.format(sequences[sequence_location])
                continue
        for index in range(len(base_percentage)):
            base_percentage[index] = (base_counts[index]/len(length_group_dic[length]) * 100)
        result += 'LENGTH = {0:d}\nFor base pos. {1:d}\nA: {2:.2f}%, T/U: {3:.2f}%, C: {4:.2f}%, G: {5:.2f}%\n\n'\
            .format(length, base_position + 1, base_percentage[0], base_percentage[1], base_percentage[2], base_percentage[3])
    return result


def write_base_proportion_file(file):
    file.write('<BASE PROPORTIONS>\n')
    for x in sequence_length_options:
        file.write(find_base_proportion(x) + '\n')


def write_length_distribution_file(file):
    file.write('<LENGTH DISTRIBUTION>\n')
    file.write('There\'s a total of {} sequences\n'.format(len(sequences)))
    for n in sequence_length_options:
        file.write('tRNA Length = {0:d}\n'.format(n))
        file.write(str(len(length_group_dic[n])) + '\n')


def sorted_secondary_structure_aa(organism_indexes, amino_acid_list):
    result = ''
    for amino_acid in amino_acid_list:
        result += '\n' + amino_acid + '\n'
        for index in organism_indexes:
            if labels[index].find(amino_acid) >= 0:
                result += labels[index] + '\n'
                result += secondary_structures[index] + '\n'
    return result


def write_sorted_secondary_structure_aa_file(file):
    amino_acids = ['Leu', 'Ser']  # fixme change this part later
    organism_names = []
    organism_names_options = []
    name_group_dic = {}
    for label in labels:
        if label.find('http') == -1:  # because of the 'XXX tRNAs were excluded' at end of the input file
            continue
        splited = label.split('/')
        organism_names.append(splited[6])
    for index, name in enumerate(organism_names):
        if not (name in organism_names_options):
            organism_names_options.append(name)
            same_organism_index = []
            for location, value in enumerate(organism_names[index:]):  # index used for efficiency
                if name == value:
                    same_organism_index.append(location + index)  # index added because enum starts at 0 again
                else:
                    break
            name_group_dic[name] = same_organism_index
    for organism in organism_names_options:
        file.write(organism + '\n')
        file.write(sorted_secondary_structure_aa(name_group_dic[organism], amino_acids) + '\n\n')


file = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input("Enter the name of the sequence file. \n")
output_file_name = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input("Enter the output file name.\n")
labels = []
sequences = []
secondary_structures = []
with open(file, 'r') as inputFile:
    for index, line in enumerate(inputFile):
        if index % 3 == 0:
            labels.append(line.strip('\n'))
        elif index % 3 == 1:
            sequences.append(line.strip('\n'))
        elif index % 3 == 2:
            secondary_structures.append(line.strip('\n'))

sequence_lengths = []  # list of length for each sequence
sequence_length_options = []  # list of categories for length
length_group_dic = {}
for sequence in sequences:
    sequence_lengths.append(len(sequence))
for index, length in enumerate(sequence_lengths):
    if not (length in sequence_length_options):
        sequence_length_options.append(length)
        same_length_sequence_index = []
        for location, value in enumerate(sequence_lengths[index:]):  # index used for efficiency
            if length == value:
                same_length_sequence_index.append(location + index)  # index added because enum starts at 0 again
        length_group_dic[length] = same_length_sequence_index
sequence_length_options = sorted(sequence_length_options, key=int)  # sorts the length options in ascending order

with open(output_file_name, 'w') as output:  # fixme must change
    write_length_distribution_file(output)

"""
    write_length_distribution_file(output)
    write_base_proportion_file(output)
    write_sorted_lengths_file(output)
"""
"""
for x in length_group_dic[3]:
    print (vloops[x])

for x in vloop_length_options:
    print(x)
    print((len(length_group_dic[x])))
"""

#  C:\Users\Yunsoo\Desktop\research\archaeal_vloops_final.txt
