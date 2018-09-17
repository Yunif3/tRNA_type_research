def find_ss_parts(input_line):
    """
    gives count of bases in each secondary structure part of type II v-loop
    :param input_line: secondary structure of a type II v-loop
    :return: list with the number of bases in each of the 5 secondary structure parts
    """
    ss_parts = []
    # part number 1
    index = input_line.find('>')
    ss_parts.append(index)
    # part number 2
    index = input_line.find('>')
    counter = 0
    while input_line[index] is '>':
        counter += 1
        index += 1
    ss_parts.append(counter)
    # part number 3
    index = input_line.find('>')
    while input_line[index] is '>':  # finds the index of first period
        index += 1
    period_counter = 0
    while input_line[index] is '.':
        period_counter += 1
        index += 1
    ss_parts.append(period_counter)
    # part number 4
    index = input_line.find('<')
    counter = 0
    while input_line[index] is '<':
        counter += 1
        index += 1
    ss_parts.append(counter)
    # part number 5
    index = input_line.find('<')
    while input_line[index] is '<':  # finds the index of first period
        index += 1
    period_counter = 0
    while input_line[index] is '.':
        period_counter += 1
        index += 1
    ss_parts.append(period_counter)

    return ss_parts


def get_stringed_ss_parts_count(input_list):  #fixme give the string explanations later
    """
    Takes a list of Type II v-loop secondary structures and prints the number of bases in each secondary structure part
    :param input_list: list of Type II v-loop secondary structures
    :return: list of bases in each of the 5 parts as a string
    """
    new_answer = []
    for line in input_list:
        if line.find('>') >= 0:
            new_answer.append(str(find_ss_parts(line)) + '\n')
        elif line == '\n':
            continue
        else:
            new_answer.append(line)
    return new_answer


def remove_html(html_included_list):
    new_list = []
    for item in html_included_list:
        if item[:4] == 'http':
            continue
        else:
            new_list.append(item)
    return new_list


def remove_secondary_structure(ss_included_list):
    new_list = []
    for item in ss_included_list:
        if any(i.isdigit() for i in item):
            new_list.append(item)
        elif item[:4] != 'http' and (item.find('.') >= 0 or item.find('<') >= 0 or item.find('>') >= 0):
            continue
        else:
            new_list.append(item)
    return new_list


def remove_index(index_included_list):
    new_list = []
    for line in index_included_list:
        if line[1:2].isdigit() and line[0:1] == '>':
            continue
        else:
            new_list.append(line)
    return new_list


def remove_organism(organism_included_list):
    new_list = []
    for line in organism_included_list:
        if line[0:1] == '#':
            continue
        else:
            new_list.append(str(line.replace('\n', '')) + '\n')
    return new_list


def fasta_format(html_included_list):
    new_list = []
    counter = 0
    for item in html_included_list:
        if item[:4] == 'http' or item[0:1] == '>':
            new_list.append('>' + str(counter) + '\n')
            counter += 1
        elif item != '\n':
            new_list.append(item)
    return new_list


def take_sequence_from_end(sequence_list, amount, direction):
    new_list = []
    for line in sequence_list:
        if line[0:1] == 'C' or line[0:1] == 'G' or line[0:1] == 'A' or line[0:1] == 'T' or line[0:1] == 'U':
            if direction == 1:
                line = line.replace('\n', '')
                new_list.append(line[:amount] + '\n')
            elif direction == -1:
                line = line.replace('\n', '')
                new_list.append(line[-amount:] + '\n')
        elif line[1:2] == '<' or line[1:2] == '>' or line[1:2] == '.':
            if direction == 1:
                new_list.append(line[:amount] + '\n')
            elif direction == -1:
                new_list.append(line[-amount:] + '\n')
        else:
            new_list.append(line)
    return new_list


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


def find_average_occurrence(sequence_list):
    new_list = []

    ss_part_list = []
    for line in sequence_list:
        if line.find('>') >= 0:
            ss_part_list.append(find_ss_parts(line))
        elif line == '\n':
            continue
        else:
            ss_part_list.append(line)
    ss_part_list.append('finished')

    index = 0
    while index < len(ss_part_list):
        if str(ss_part_list[index][0]).isdigit():
            sums = [0] * 5
            average = [0] * 5
            total_size = 0
            while str(ss_part_list[index][0]).isdigit():
                for n in range(len(ss_part_list[index])):
                    sums[n] += ss_part_list[index][n]
                index += 1
                total_size += 1
            for n, sum in enumerate(sums):
                average[n] = sum / total_size
                new_list.append(str(average[n]) + '\n')
        else:
            new_list.append(ss_part_list[index])
            index += 1
    return new_list


def find_average_difference(sequence_list):
    new_list = []
    index = 0
    no_newLine = []
    for line in sequence_list:
        no_newLine.append(line.replace('\n', ''))
    while index < len(no_newLine):
        if no_newLine[index] == 'Leu':
            index += 1
            differences = [0] * 5
            for n in range(5):
                differences[n] += float(no_newLine[index])
                index += 1

            while no_newLine[index] != 'Ser':
                index += 1
            index += 1
            for n in range(5):
                differences[n] -= float(no_newLine[index])
                index += 1
            new_list.append(str(differences) + '\n')
        else:
            new_list.append(no_newLine[index] + '\n')
            index += 1
    return new_list


def isolate_selected_lengths(mixed_length_list, lengths):  # the lines must be in pairs
    new_list = []
    copied_list = []
    for line in mixed_length_list:
        copied_list.append(line)
    index = 0
    while index < len(copied_list) - 1:
        if copied_list[index][0:1] == '>' or copied_list[index][0:1] == '#':
            sequence = copied_list[index+1].replace('\n', "")
            if len(sequence) in lengths:
                new_list.append(copied_list[index])
                new_list.append(sequence + '\n')
        index += 1
    return new_list


def find_complement(original_sequence_list): #fixme change the if statements later
    new_list = []
    for original_sequence in original_sequence_list:
        if original_sequence[0:1] == '>' or original_sequence[0:1] == '#':
            new_list.append(original_sequence)
        else:
            complement = ''
            for base in original_sequence:
                if base == 'A':
                    complement += 'T'
                elif base == 'T' or base == 'U':
                    complement += 'A'
                elif base == 'C':
                    complement += 'G'
                elif base == 'G':
                    complement += 'C'
                elif base == 'N':
                    complement += 'N'
            new_list.append(complement + '\n')
    return new_list


def reverse_sequence(original_sequence_list):  # fixme same issue as above
    new_list = []
    for original_sequence in original_sequence_list:
        if original_sequence[0:1] == '>' or original_sequence[0:1] == '#':
            new_list.append(original_sequence)
        else:
            original_sequence = original_sequence.replace('\n', '')
            new_list.append(original_sequence[::-1] + '\n')
    return new_list


def replace_uracine(U_included_list):
    new_list = []
    for original_sequence in U_included_list:
        if original_sequence[0:1] == '>' or original_sequence[0:1] == '#':
            new_list.append(original_sequence)
        else:
            new_sequence = ''
            for base in original_sequence:
                if base == 'U':
                    new_sequence += 'T'
                else:
                    new_sequence += base
            new_list.append(new_sequence + '\n')
    return new_list


def remove_end_sequences(original_list, amount, direction):
    new_list = []
    for line in original_list:
        if line[0:1] == 'C' or line[0:1] == 'G' or line[0:1] == 'A' or line[0:1] == 'T' or line[0:1] == 'U':
            if direction == 1:
                line = line.replace('\n', '')
                new_list.append(line[amount:] + '\n')
            elif direction == -1:
                line = line.replace('\n', '')
                new_list.append(line[:-amount] + '\n')
        elif line[1:2] == '<' or line[1:2] == '>' or line[1:2] == '.':
            if direction == 1:
                new_list.append(line[amount:] + '\n')
            elif direction == -1:
                new_list.append(line[:-amount] + '\n')
        else:
            new_list.append(line)
    return new_list


file = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the input file.\n')
outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the output file.\n')
answer = []
with open(file, 'r') as input:
    answer = remove_html(input)
    answer = remove_secondary_structure(answer)
    answer = replace_uracine(answer)
    #answer = remove_index(answer)
    answer = remove_organism(answer)

    #answer = isolate_selected_lengths(answer, [7])
    answer_copy = answer[:]
    answer = add_sequences(take_sequence_from_end(answer, 7, 1), take_sequence_from_end(answer_copy, 7, -1))
    #answer = remove_end_sequences(answer, 1, 1)
    #answer = remove_end_sequences(answer, 1, -1)
    #answer = remove_end_sequences(answer, 1, 1)
    #answer = take_sequence_from_end(answer, 6, 1)
    answer = isolate_selected_lengths(answer, [14])
    #answer = reverse_sequence(answer)
    #answer = find_complement(answer)


with open(outputFile, 'w') as output:
    for line in answer:
        output.write(line)

