no_enter = []
first = True
temp = ""
with open('C:\\Users\\Yunsoo\\Desktop\\research\\archaeal_tRNA.txt', 'r') as myFile:
    for line in myFile:
        if line[0] == '>':
            if first:
                first = False
            else:
                no_enter.append(temp)
                temp = ""
            line = line.strip("\n")
            no_enter.append(line)
        else:
            line = line.strip('\n')
            temp += line.upper()
    no_enter.append(temp)
with open ('C:\\Users\\Yunsoo\\Desktop\\research\\archaeal_tRNA_no_enter.txt', 'w') as output:
    for lines in no_enter:
        output.write(lines)
        output.write("\n")
