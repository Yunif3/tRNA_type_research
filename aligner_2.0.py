from random import shuffle


def get_permuted_list(sequence_list):
    """
    Takes in a sequence list, shuffles the base in each sequence, then returns permuted sequence list
    :param sequence_list: sequence list with bases in their original position
    :return: permuted sequence list
    """
    permuted_list = []
    for sequence in sequence_list:
        s = list(sequence)
        shuffle(s)
        permuted_list.append(''.join(s))
    return permuted_list


def get_permutated_sequence_distance(subject_list, query_list):
    """
    Takes in subject list and query list, uses get_permuted_list() on them, finds the score between two scores,
    then uses those scores to find the permuted evolutionary distance.
    :param subject_list: user inputted subject sequence list
    :param query_list: user inputted query sequence list
    :return: permuted evolutionary distance
    """
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
    """
    finds the evolutionary distance based on the scores between two sequence lists
    :param score_list: list of scores found between two sequence lists
    :param m: the length of each sequence
    :return: evolutionary distance
    """
    score_sum = 0
    for score in score_list:
        score_sum += (score / m) ** 2
    return score_sum ** .5


def find_all_distances(subject_list, query_list):  # fixme
    """
    Finds original evolutionary distance and 1000 permuted evolutionary distances.
    :param subject_list: user inputted subject sequence list
    :param query_list: user inputted query sequence list
    :return: list of original evolutionary distance and 1000 permuted evolutionary distances.
    """
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
    """
    finds how what proportion of permuted distances are smaller than the original distance
    :param distance_list: distance list with original distance being first with 1000 permuted distances following
    :return: p-value
    """
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

subject_list = []
query_list = []
scores = []

with open(inputFile1, 'r') as input1:
    copied_list = []
    for line in input1:
        copied_list.append(line)
    for i, line in enumerate(copied_list):
        if (line[0:1] == '>' or line[0:1] == '#') and len(copied_list[i + 1]) == len(copied_list[1]):
            subject_list.append(copied_list[i + 1].replace('\n', ''))

with open(inputFile2, 'r') as input2:
    copied_list = []
    for line in input2:
        copied_list.append(line)
    for i, line in enumerate(copied_list):
        if (line[0:1] == '>' or line[0:1] == '#') and len(copied_list[i + 1]) == len(copied_list[1]):
            query_list.append(copied_list[i + 1].replace('\n', ''))

with open(outputFile, 'w') as output:
    """
    sequence_count = 0
    if len(subject_list) < len(query_list):
        sequence_count = len(subject_list)
    else:
        sequence_count = len(query_list)

    shuffle(subject_list)
    shuffle(query_list)
    random_subjects = subject_list[0: sequence_count]
    random_queries = query_list[0: sequence_count]
    distances = find_all_distances(random_subjects, random_queries)
    p_value = find_p_value(distances)
    output.write("{0:.5f}\n".format(p_value))
    for dist in distances:
        output.write("{0:.5f}\n".format(dist))
    print(p_value)
    """
    counter = 0
    while counter < 50:
        sequence_count = 0
        if len(subject_list) < len(query_list):
            sequence_count = len(subject_list)
        else:
            sequence_count = len(query_list)

        shuffle(subject_list)
        shuffle(query_list)
        random_subjects = subject_list[0: sequence_count]
        random_queries = query_list[0: sequence_count]
        """
        # finds original distances
        original_scores = []
        for n, subject in enumerate(random_subjects):
            original_scores.append(get_score(subject, random_queries[n]))
        original_distance = get_evolutionary_distance(original_scores, len(random_subjects[0]))
        output.write("{0:.5f}\n".format(original_distance))
        counter += 1
        print('counter = ' + str(counter))
        """
        # finds p-value
        distances = find_all_distances(random_subjects, random_queries)
        p_value = find_p_value(distances)
        output.write("{0:.5f}\n".format(p_value))
        counter += 1
        print('counter = ' + str(counter))
