import requests
from bs4 import BeautifulSoup
import csv


def isolate_secondary_structure(string):
    structure_marks = ""
    for char in string:
        if char == '<' or '>' or '.':
            structure_marks += char
    return structure_marks


def edit_name (tRNA_name):
    new_parts = []
    tRNA_name = tRNA_name.replace('-', ' ')
    tRNA_name = tRNA_name.replace('sp. ', '')
    tRNA_name = tRNA_name.replace('str. ', '')
    tRNA_name = tRNA_name.replace('.', ' ')
    tRNA_name = tRNA_name.replace('/', ' ')
    name_parts = tRNA_name.split(' ')
    for word_count, part in enumerate(name_parts):
        if word_count == 0 or (word_count < 2 and not any(i.isupper() for i in part)):
            new_parts.append(part[0:4])
        else:
            new_parts.append(part)
    return '_'.join(new_parts)


def find_sequence_end_index(secondary_structure, loop_type, interval): #interval must be 1 or -1
    index = -1
    stem_counter = 0
    stem_status = 0
    first_stem_base = True

    if interval == 1:
        stem_counter_requirement = 0
        if loop_type == 'vLoop':
            stem_counter_requirement = 2
        elif loop_type == 'acLoop':
            stem_counter_requirement = 1

        acceptor_start_index = 0
        while not secondary_structure[acceptor_start_index] == '>':
            acceptor_start_index += 1

        index = acceptor_start_index + 7
        while stem_counter < stem_counter_requirement:
            if secondary_structure[index] == '>':
                stem_status += 1
                first_stem_base = False
            elif secondary_structure[index] == '<':
                stem_status -= 1
            if (stem_status == 0) and (first_stem_base is False):
                stem_counter += 1
                first_stem_base = True
            index += 1

        while secondary_structure[index] != '>' and loop_type != 'vLoop':  # fixme
            index += 1

    elif interval == -1:
        stem_counter_requirement = 0
        if loop_type == 'vLoop':
            stem_counter_requirement = 1

        acceptor_start_index = len(secondary_structure) - 1
        while not secondary_structure[acceptor_start_index] == '<':
            acceptor_start_index -= 1
        index = acceptor_start_index - 7

        if loop_type == 'tLoop':  # fixme this is because the tLoop stem starts right after the 3' acceptor stem
            return index

        while stem_counter < stem_counter_requirement:
            if secondary_structure[index] == '>':
                stem_status += 1
            elif secondary_structure[index] == '<':
                stem_status -= 1
                first_stem_base = False
            if (stem_status == 0) and (first_stem_base is False):
                stem_counter += 1
                first_stem_base = True
            index -= 1

        while secondary_structure[index] != '<' and loop_type != 'vLoop':  # fixme
            index -= 1
    return index


def select_vLoop():
    global chosen_sequence
    global chosen_secondary_structure
    vLoop_start_index = find_sequence_end_index(secondary_structure,'vLoop', 1)
    vLoop_end_index = find_sequence_end_index(secondary_structure,'vLoop', -1) + 1  # since end is excluded by [x:y]
    chosen_sequence = mature_tRNA_sequence[vLoop_start_index: vLoop_end_index]
    chosen_secondary_structure = secondary_structure[vLoop_start_index: vLoop_end_index]


def select_acLoop():
    global chosen_sequence
    global chosen_secondary_structure
    acLoop_start_index = find_sequence_end_index(secondary_structure, 'acLoop', 1)
    vLoop_start_index = find_sequence_end_index(secondary_structure, 'vLoop', 1)
    acLoop_end_index = vLoop_start_index  # start of vLoop is end of acLoop
    chosen_sequence = mature_tRNA_sequence[acLoop_start_index: acLoop_end_index]
    chosen_secondary_structure = secondary_structure[acLoop_start_index: acLoop_end_index]


def select_tLoop():
    global chosen_sequence
    global chosen_secondary_structure
    vLoop_end_index = find_sequence_end_index(secondary_structure, 'vLoop', -1)
    tLoop_start_index = vLoop_end_index + 1 # tloop starts right after vloop ends
    tLoop_end_index = find_sequence_end_index(secondary_structure, 'tLoop', -1) + 1   # since end is excluded by [x:y]
    chosen_sequence = mature_tRNA_sequence[tLoop_start_index: tLoop_end_index]
    chosen_secondary_structure = secondary_structure[tLoop_start_index: tLoop_end_index]


def select_all():
    global chosen_sequence
    global chosen_secondary_structure
    chosen_sequence = mature_tRNA_sequence
    chosen_secondary_structure = secondary_structure


def select_p3_stem():
    global chosen_sequence
    global chosen_secondary_structure
    acLoop_start_index = find_sequence_end_index(secondary_structure, 'acLoop', 1)
    p3_start_index = acLoop_start_index - 4
    p3_end_index = acLoop_start_index + 1  # since end is excluded by [x:y]
    chosen_sequence = mature_tRNA_sequence[p3_start_index : p3_end_index]
    chosen_secondary_structure = secondary_structure[p3_start_index : p3_end_index]


tRNA_url_info = []
file = 'C:\\Users\\Yunsoo\\Desktop\\research\\csv_files\\' + str(input('Enter the csv file name.\n'))
outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + str(input('Enter the output file name.\n'))
selected_portion = input('Enter the portion to be extracted. (vLoop/acLoop/tLoop/p3_stem/all)\n')

with open(file, 'r') as csvFile:  # must be changed
    file_reader = csv.reader(csvFile, delimiter = ',')
    for row in file_reader:
        tRNA_url_info.append(row)

with open(outputFile, 'w') as output:  # must be changed
    progress_counter = 0
    total_task = len(tRNA_url_info)
    exclusion_counter = 0
    for url_parts in tRNA_url_info:
        try:
            underscored_name = edit_name(url_parts[0])
            tRNA_ID = url_parts[1]
            url = "http://lowelab.ucsc.edu/GtRNAdb2/genomes/archaea/" + underscored_name + "/genes/" + tRNA_ID + ".html" #fixme set as archaea for now
            page = requests.get(url)
            if page.status_code != 200:
                print(url_parts[0])
                exclusion_counter += 1
                progress_counter += 1
                print(str(progress_counter) + ' / ' + str(total_task) + ' done.')
                continue
            soup = BeautifulSoup(page.content, 'html.parser')
            pre = soup.select("div.panel pre")  # gonna use pre[1] and pre[2]
            mature_tRNA_sequence = pre[1].get_text().upper()
            secondary_structure = isolate_secondary_structure(pre[2].get_text())

            chosen_sequence = ''
            chosen_secondary_structure = ''

            if selected_portion == 'vLoop':  # very important
                select_vLoop()
            elif selected_portion == 'acLoop':
                select_acLoop()
            elif selected_portion == 'tLoop':
                select_tLoop()
            elif selected_portion == 'p3_stem':
                select_p3_stem()
            elif selected_portion == 'all':
                select_all()

            output.write(str(url) + '\n')
            output.write(str(chosen_sequence) + '\n')
            output.write(str(chosen_secondary_structure) + '\n')
            progress_counter += 1
            print(str(progress_counter) + ' / ' + str(total_task) + ' done.')
        except Exception:
            print(url_parts[0])
            exclusion_counter += 1
            progress_counter += 1
            print(str(progress_counter) + ' / ' + str(total_task) + ' done.')
            continue
    last_comment = str(exclusion_counter) + ' tRNAs were excluded \n'
    output.write(last_comment)
print('task completed')
