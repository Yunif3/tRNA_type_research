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


def select_5end_stem():
    global chosen_sequence
    global chosen_secondary_structure
    chosen_sequence = mature_tRNA_sequence[:7]
    chosen_secondary_structure = secondary_structure[:7]


def select_3end_stem():
    global chosen_sequence
    global chosen_secondary_structure
    acceptor_end_index = len(secondary_structure) - 1
    while not secondary_structure[acceptor_end_index] == '<':
        acceptor_end_index -= 1
    acceptor_start_index = acceptor_end_index - 6
    chosen_sequence = mature_tRNA_sequence[acceptor_start_index: acceptor_end_index + 1]
    chosen_secondary_structure = secondary_structure[acceptor_start_index: acceptor_end_index + 1]


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


def select_p5_stem():
    global chosen_sequence
    global chosen_secondary_structure
    acLoop_start_index = find_sequence_end_index(secondary_structure, 'acLoop', 1)
    p5_start_index = acLoop_start_index - 5
    p5_end_index = acLoop_start_index  # since end is excluded by [x:y]
    chosen_sequence = mature_tRNA_sequence[p5_start_index: p5_end_index]
    chosen_secondary_structure = secondary_structure[p5_start_index: p5_end_index]


task_type = input("Are you extracting portions from tRNA?\n")
if task_type == 'yes':
    file = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + str(input('Enter the input file name.\n'))
    outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + str(input('Enter the output file name.\n'))
    selected_portion = input('Enter the portion to be extracted.\n')

    tRNA_info = []
    with open(file, 'r') as input:
        for line in input:
            if line != '\n':
                tRNA_info.append(line)

    with open(outputFile, 'w') as output:
        tRNA_count = len(tRNA_info) // 4
        index = 0
        exclusion_counter = 0
        while index < tRNA_count:
            try:
                organism = tRNA_info[index * 4]
                url = tRNA_info[(index * 4) + 1]
                mature_tRNA_sequence = tRNA_info[(index * 4) + 2]
                secondary_structure = tRNA_info[(index * 4) + 3]

                chosen_sequence = ''
                chosen_secondary_structure = ''

                if selected_portion == '5end_stem':
                    select_5end_stem()
                elif selected_portion == 'vLoop':
                    select_vLoop()
                elif selected_portion == 'acLoop':
                    select_acLoop()
                elif selected_portion == 'tLoop':
                    select_tLoop()
                elif selected_portion == 'p5_stem':
                    select_p5_stem()
                elif selected_portion == '3end_stem':
                    select_3end_stem()
                elif selected_portion == 'all':
                    select_all()

                if chosen_sequence == '\n':
                    exclusion_counter += 1
                    index += 1
                    continue

                output.write('>' + str(index) + '\n')
                output.write('#' + str(organism))  # already has \n
                output.write(url)  # already has \n
                output.write(chosen_sequence + '\n')
                output.write(chosen_secondary_structure + '\n')
                index += 1
            except Exception:
                print(url)
                exclusion_counter += 1
                index += 1
                continue

        print(str(exclusion_counter) + ' sequences were excluded.\n')

elif task_type == 'no':
    organism_domain = str(input("Is it archaea or bacteria?\n"))
    file = 'C:\\Users\\Yunsoo\\Desktop\\research\\csv_files\\' + str(input('Enter the csv file name.\n'))
    outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + str(input('Enter the output file name.\n'))
    tRNA_urls = []
    organism_names = []
    with open(file, 'r') as csvFile:  # must be changed
        file_reader = csv.reader(csvFile, delimiter = ',')
        for row in file_reader:
            underscored_name = edit_name(row[0])
            tRNA_ID = row[1]
            url = "http://lowelab.ucsc.edu/GtRNAdb2/genomes/" + organism_domain + "/" + underscored_name + "/genes/" + tRNA_ID + ".html"
            # fixme this is set as archaea right now
            tRNA_urls.append(url)
            organism_names.append(underscored_name)

    with open(outputFile, 'w') as output:  # must be changed
        progress_counter = 0
        total_task = len(tRNA_urls)
        exclusion_counter = 0
        for index, url in enumerate(tRNA_urls):
            try:
                page = requests.get(url)
                if page.status_code != 200:
                    print(url)
                    exclusion_counter += 1
                    progress_counter += 1
                    print(str(progress_counter) + ' / ' + str(total_task) + ' done.')
                    continue
                soup = BeautifulSoup(page.content, 'html.parser')
                pre = soup.select("div.panel pre")  # gonna use pre[1] and pre[2]
                mature_tRNA_sequence = pre[1].get_text().upper()
                secondary_structure = isolate_secondary_structure(pre[2].get_text())

                output.write(str(organism_names[index]) + '\n')
                output.write(str(url) + '\n')
                output.write(str(mature_tRNA_sequence) + '\n')
                output.write(str(secondary_structure) + '\n')
                progress_counter += 1
                print(str(progress_counter) + ' / ' + str(total_task) + ' done.')
            except Exception:
                print(url)
                exclusion_counter += 1
                progress_counter += 1
                print(str(progress_counter) + ' / ' + str(total_task) + ' done.')
                continue
        last_comment = str(exclusion_counter) + ' tRNAs were excluded \n'
        output.write(last_comment)
        print('task completed')
