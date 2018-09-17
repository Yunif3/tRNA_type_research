def find_complement (original_sequence):
    complement = ""
    for base in original_sequence:
        if base == 'A':
            complement += 'T'
        elif base == 'T':
            complement += 'A'
        elif base == 'C':
            complement += 'G'
        elif base == 'G':
            complement += 'C'
    return complement


def reverse(original):
    return original[::-1]


def check_pairing_error(original, variation, error_threshold): #fixme
    error_count = 0
    i = 0
    while i+7 < len(original):
        base_sequence = original[i:i+7]
        for n in range(len(base_sequence)):
            if not base_sequence[n] == variation[n]:
                error_count += 1
        if error_count <= error_threshold:
            return base_sequence
        i += 1
        error_count = 0
    return "error in finding complementing stem."


inputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of input file.\n')
outputFile = 'C:\\Users\\Yunsoo\\Desktop\\research\\' + input('Enter the name of output file.\n')

acceptor_stems = []
with open(inputFile, 'r') as input:
    for line in input:
        if line[0] == '>':
            acceptor_stems.append(line)
        else:
            start_stem = line[:7]
            # acceptor_stems.append(start_stem)
            start_stem_complement = find_complement(start_stem)

            end_stem = line[-20:]
            if end_stem.find(reverse(start_stem_complement)) >= 0: #reverse is used due to the fold of tRNA
                acceptor_stems.append(reverse(start_stem_complement))
            elif (len(check_error(end_stem, reverse(start_stem_complement), 1)) == 7):
                acceptor_stems.append(check_error(end_stem, reverse(start_stem_complement), 1))
                #  acceptor_stems.append("has 1 non-complementary base")
            elif (len(check_error(end_stem, reverse(start_stem_complement), 2)) == 7):
                acceptor_stems.append(check_error(end_stem, reverse(start_stem_complement), 2))
                #  acceptor_stems.append("has 2 non-complementary base")
            #  else:
                #  acceptor_stems.append("error in finding complementing stem.")

with open(outputFile, 'w') as output:
    for line in acceptor_stems:
        output.write(line)
        output.write('\n')
