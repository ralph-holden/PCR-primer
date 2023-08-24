#OTHER BASIC FUNCTIONS
def cut_from_string(remove, string):
    'Creates a new string with the requested string removed'
    cut_string = ''
    for k in string:
        if k not in remove:
            cut_string = cut_string + k
    return cut_string

#def test(string1, string2):
#    'Check for complementary pairs for one pair only, to be used in continious match'
#    for i in range(len(string1)):
#        if string1[i] in 'AT' and string2[i] in 'AT':
#            if string1[i] != string2[i]:
#                return False
#        if string1[i] in 'GC' and string2[i] in 'GC':
#            if string1[i] != string2[i]:
#                return False
#    else:
#        return True
    
# def reverse_string(string):
#    'In the name'
#    new_string = ''
#    for i in range(len(string)):
#        new_string = new_string + string[len(string)-1-i]
#    return new_string
#reverse_string
#rs = reverse_string

#REQUESTED FUNCTIONS
def readin_fasta(filename):
    'From name/ path of file, returns all DNA in single string with only ATGC (nothing else eg. spaces & dashes)'
    stream1=open(filename,'r')

    _data_ = ''
    for line in stream1:
        _data_ = _data_ + line

    great_data = ''
    for n in _data_:
        if n in 'ATGC':
            great_data = great_data + n
    great_data = great_data[1:]
    return great_data


def CG_edge(string):
    'Tests for string ending in C or G'
    if string[0] in 'CG' and string[-1] in 'CG':
        return True
    else:
        return False
    
    
def CG_count(string):
    'Returns number of Cs&Gs in string'
    count = 0
    for i in string:
        if i in 'GC':
            count = count + 1
    return count


def reverse_complement(input_string):
    'Returns the complementary string (in reverse order) for a given string'
    output_string = ''
    for i in input_string:
        for m in ['AT','GC']:
            if i in m:
                output_string = cut_from_string(i,m) + output_string
    return output_string

def complement5(string1,string2):
    'Given two strings, returns False if any 5 continuous parts are matching'
    for i in range(len(string1)-4):
        for k in range(len(string2)-4):
            if string1[i:i+5] == reverse_complement(string2)[k:k+5]: #CHECK WHICH SYNTAX ORDER THIS NEEDS
                return False
    else:
        return True

#OTHER MORE ADVANCED FUNCTIONS
def no_hairpin(string):
    'Adapts one string, for use of complement5 function'
    string1 = string[:10]
    string2 = string[10:]
    if complement5(string1,string2) == False:
        return False
    else:
        return True
    
def CG_count_check(string):
    if 8 <= CG_count(string) <= 12:
        return True
    else:
        return False

def find_PCR_primer_true(input_filename, input_two_integer_numbers):
    
    #finding data & range from inputs
    DATA_ = readin_fasta(input_filename)
    
    number1 = int(input_two_integer_numbers.split(' ')[0])
    number2 = int(input_two_integer_numbers.split(' ')[1])
    
    string1_DNA_35 = DATA_[number1:number2]
    string2_DNA_35 = reverse_complement(DATA_[number1:number2])
    
    part_string1_primer_35 = ''
    part_string2_primer_35 = ''
    
    for i in range(number2-number1-19):
        if CG_edge(string1_DNA_35[i:i+20]):
            if CG_count_check(string1_DNA_35[i:i+20]):
                if no_hairpin(string1_DNA_35[i:i+20]):
                    part_string1_primer_35 = reverse_complement(string1_DNA_35[i:i+20])
            
        if CG_edge(string2_DNA_35[i:i+20]):
            if CG_count_check(string2_DNA_35[i:i+20]):
                if no_hairpin(string2_DNA_35[i:i+20]):
                    part_string2_primer_35 = reverse_complement(string2_DNA_35[i:i+20])
                        
        if complement5(part_string1_primer_35,part_string2_primer_35):
            if part_string1_primer_35 != '' and part_string2_primer_35 != '':
                string1_primer_35 = part_string1_primer_35
                string2_primer_35 = part_string2_primer_35
                SPS = 'Start primer sequence : ' + string1_primer_35
                RPS = 'Reverse primer sequence : ' + string2_primer_35
                print(SPS)
                print(RPS)
                return SPS , RPS
            
    if part_string1_primer_35 != '' or part_string2_primer_35 != '':
        if complement5(part_string1_primer_35,part_string2_primer_35):
            string1_primer_35 = part_string1_primer_35
            string2_primer_35 = part_string2_primer_35
            SPS = 'Start primer sequence : ' + string1_primer_35
            RPS = 'Reverse primer sequence : ' + string2_primer_35
            print(SPS)
            print(RPS)
            return SPS , RPS
                  
    elif part_string1_primer_35 == '' or part_string2_primer_35 == '':
        SPS = 'Start primer sequence : ' + string1_primer_35
        RPS = 'Reverse primer sequence : ' + string2_primer_35
        print(SPS)
        print(RPS)
        return SPS , RPS
    

if __name__=="__main__":
#INPUTS REQUIRED
    input_filename = input('Please give the file name ')
    input_two_integer_numbers = input('Please give the number range, starting with the lowest ')

    find_PCR_primer_true(input_filename, input_two_integer_numbers)

input('Press return to close the window.')