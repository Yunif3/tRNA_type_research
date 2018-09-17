def find_ss_parts (input_line):
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
        if item[:4] != 'http' and item.find('.') >= 0 or item.find('<') >= 0 or item.find('>') >= 0:
            continue
        else:
            new_list.append(item)
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


def take_five_from_end(sequence_list, direction):
    new_list = []
    for line in sequence_list:
        if line[0:1] == 'C' or line[0:1] == 'G' or line[0:1] == 'a' or line[0:1] == 'T' or line[0:1] == 'U':
            if direction == 1:
                new_list.append(line[:5] + '\n')
            elif direction == -1:
                new_list.append(line[-5:] + '\n')
        elif line[0:2] == '<<' or line[0:2] == '>>':
            new_list.append(line[:5] + '\n')
        else:
            new_list.append(line)
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


file = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the structure_organism file.\n')
outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the output file.\n')
answer = []
with open(file, 'r') as input:
    answer = fasta_format(input)
    answer = take_five_from_end(answer, 1)


with open(outputFile, 'w') as output:
    for line in answer:
        output.write(line)

#  archaeal_tLoops_SER_LEU_new_organized.txt
#  ss_noHTML_test.txt