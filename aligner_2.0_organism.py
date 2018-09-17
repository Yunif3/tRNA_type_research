from random import shuffle

#fixme must go through a unit test
def get_permuted_list(sequence_list):
    permuted_list = []
    for sequence in sequence_list:
        s = list(sequence)
        shuffle(s)
        permuted_list.append(''.join(s))
    return permuted_list


def get_permutated_sequence_distance(subject_list, query_list):
    subject_permutations = get_permuted_list(subject_list)
    query_permutations = get_permuted_list(query_list)
    permutation_scores = []
    index = 0
    while index < len(subject_list):
        permutation_scores.append(get_score(subject_permutations[index], query_permutations[index]))
        index += 1
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
        if base != query[index]:
            mismatches += 1
    return mismatches


def get_evolutionary_distance(score_list, m):
    score_sum = 0
    for score in score_list:
        score_sum += (score / m) ** 2
    return score_sum ** .5


def find_all_distances(subject_list, query_list):  # fixme
    distances = []
    original_scores = []
    subject_sequences = subject_list
    query_sequences = query_list

    for n, subject in enumerate(subject_sequences):
        original_scores.append(get_score(subject, query_sequences[n]))
    distances.append(get_evolutionary_distance(original_scores, len(subject_sequences[0])))

    counter = 0
    while counter < 1000:
        distances.append(get_permutated_sequence_distance(subject_sequences, query_sequences))
        counter += 1
        print(counter)
    return distances


def find_p_value(distance_list):
    counter = 0
    original_distance = distance_list[0]
    for dist in distance_list:
        if dist < original_distance:
            counter += 1
    return (counter + 1) / (len(distance_list))  # no +1 since original dist is in the dist list too


user_input1 = input('Enter the name of the first input file.\n')
user_input2 = input('Enter the name of the second input file.\n')
inputFile1 = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + user_input1
inputFile2 = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + user_input2
outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\sa_2.0_results\\' + user_input1[:-4] +'_vs_' + user_input2[:-4] + '.txt'

subject_dict = {}
query_dict = {}
scores = []

with open(inputFile1, 'r') as input1:
    copied_list = []
    for line in input1:
        copied_list.append(line)
    for i, line in enumerate(copied_list):
        if (line[0:1] == '>' or line[0:1] == '#') and len(copied_list[i + 1]) == len(copied_list[1]):
            if line not in subject_dict:
                subject_dict[line] = []
                subject_dict[line].append(copied_list[i + 1].replace('\n', ''))
            else:
                subject_dict[line].append(copied_list[i + 1].replace('\n', ''))
            query_dict[line] = []

with open(inputFile2, 'r') as input2:
    copied_list = []
    for line in input2:
        copied_list.append(line)
    for i, line in enumerate(copied_list):
        if line in query_dict:
            query_dict[line].append(copied_list[i + 1].replace('\n', ''))

with open(outputFile, 'w') as output:
    subject_list = []
    query_list = []
    for key in list(subject_dict.keys()):
        if query_dict[key] != []: # got to put the smaller list as input1
            subjects = subject_dict[key]
            queries = query_dict[key]
            shuffle(subjects)
            shuffle(queries)
            subject_list += subjects
            query_list += queries[0:len(subjects)]
    distances = find_all_distances(subject_list, query_list)
    p_value = find_p_value(distances)
    output.write("{0:.5f}\n".format(p_value))
    for dist in distances:
        output.write("{0:.5f}\n".format(dist))
    print(p_value)

