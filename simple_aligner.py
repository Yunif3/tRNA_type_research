from random import shuffle


def get_all_permutations(sequence, permutation_list, base=0):
    """
    fixme includes the original sequence too
    It gives ALL combinations ( with duplicates). It needs an list outside to keep all the permutations
    :param sequence: A string to be permutated
    :param base: always keep as default
    """

    if base == len(sequence):
        permutation_list.append(''.join(sequence))
    for i in range(base, len(sequence)):
        copy = [b for b in sequence]
        copy[base], copy[i] = copy[i], copy[base]
        get_all_permutations(copy, permutation_list, base + 1)


def get_permutated_sequence_distance(subject, query):
    subject_permutations = []
    query_permutations = []
    permutation_scores = []
    get_all_permutations(subject, subject_permutations)
    get_all_permutations(query, query_permutations)
    subject_permutations = list(set(subject_permutations))  # removes duplicates
    query_permutations = list(set(query_permutations))
    for subject_permutation in subject_permutations:
        for query_permutation in query_permutations:
            permutation_scores.append(get_score(subject_permutation, query_permutation))
    return get_evolutionary_distance(permutation_scores, len(subject_permutations[0]))



def get_score(subject, query):
    """
    assumes that the two sequences are the same length
    :param subject: string coming from seq list 1. What we are trying to prove to be homologous
    :param query: string coming from seq list 2. What our subject is homologous to
    :return: the score based on number of mismatch (+1)
    """
    mismatches = 0
    for index, base in enumerate(subject):
        if (base != query[index]):
            mismatches += 1
    return mismatches


def get_evolutionary_distance(score_list, m):
    score_sum = 0  # (d/m)**2
    if m == 0:
        input()
    for score in score_list:
        score_sum += (score/m)**2
    return ((score_sum**.5) * 10000)/len(score_list)


def write_all_distances(file, subject_dict, query_dict):  # fixme
    first_key = list(subject_dict.keys())[0]
    output.write('{0:.3f}\n'.format(get_evolutionary_distance(scores, len(subject_dict[first_key][0]))))
    for key in subject_dict.keys():
        for subject in subject_dict[key]:
            for query in query_dict[key]:
                output.write('{0:.3f}\n'.format(get_permutated_sequence_distance(subject, query)))


def find_p_value(subject_dict, query_dict):  # fixme
    counter = 0
    first_key = list(subject_dict.keys())[0]
    original_dist = get_evolutionary_distance(scores, len(subject_dict[first_key][0]))
    permutation_dist = []
    for key in subject_dict.keys():
        for subject in subject_dict[key]:
            for query in query_dict[key]:
                permutation_dist.append(get_permutated_sequence_distance(subject, query))
    for dist in permutation_dist:
        if dist < original_dist:
            counter += 1
    return (counter + 1)/(len(permutation_dist) + 1)

"""
def same_tRNA_input():
    subject_list = []
    query_dict = {}
    scores = []
    
    with open(inputFile1, 'r') as input1:
        copied_list = []
        for line in input1:
            copied_list.append(line)
        for i, line in enumerate(copied_list):
            if line[0:1] == 'C' or line[0:1] == 'G' or line[0:1] == 'A' or line[0:1] == 'T' or line[0:1] == 'U':
                subject_list.append(line.replace('\n', ''))
                tRNA_index_list.append(copied_list[i - 1])

    with open(inputFile2, 'r') as input2:
        copied_list = []
        for line in input2:
            copied_list.append(line)
        for i, line in enumerate(copied_list):
            if (copied_list[i - 1] in tRNA_index_list) and (line[0:1] == 'C' or line[0:1] == 'G' or line[0:1] == 'A' or line[0:1] == 'T' or line[0:1] == 'U'):
                sequence_list2.append(line.replace('\n', ''))
"""
inputFile1 = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the first input file.\n')
inputFile2 = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the second input file.\n')
outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of the output file.\n')

subject_dict = {}
query_dict = {}
scores = []

with open(inputFile1, 'r') as input1:
    copied_list = []
    for line in input1:
        copied_list.append(line)
    for i, line in enumerate(copied_list):
        if (line[0:1] == '>' or line[0:1] == '#') and len(copied_list[i + 1]) == len(copied_list[1]):
            if not line in subject_dict:
                subject_dict[line] = []
            else:
                subject_dict[line].append(copied_list[i + 1].replace('\n', ''))
            if line[0:1] == '>':  # fixme get rid of this later. This is to prove a point on the old method
                subject_dict[line].append(copied_list[i + 1].replace('\n', ''))
            query_dict[line] = []

with open(inputFile2, 'r') as input2:
    copied_list = []
    for line in input2:
        copied_list.append(line)
    for i, line in enumerate(copied_list):
        if line in query_dict:
            query_dict[line].append(copied_list[i + 1].replace('\n', ''))

for key in subject_dict.keys():
    for subject in subject_dict[key]:
        for query in query_dict[key]:
            scores.append(get_score(subject, query))


with open(outputFile, 'w') as output:
    write_all_distances(output, subject_dict, query_dict)
print(find_p_value(subject_dict, query_dict))
