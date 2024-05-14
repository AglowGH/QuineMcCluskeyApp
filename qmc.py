
def int_to_str_bin(number:int,size:int)->str:
    return format(number,f'0{size}b')

def bits_on(str_bin:str)->int:
    return str_bin.count('1')

def group_rows(rows:list)->dict:
    group = {}
    for row in rows:
        b_on = bits_on(row)
        if b_on in group:
            group[b_on].append([[row],True,row])
        else:
            group[b_on] = [[[row],True,row]]
    return group

def compare_and_chage(b1:str,b2:str)->str:
    counter = 0
    new_b = ''
    for i in range(0,b1.__len__()):
        if b1[i] != b2[i]:
            new_b = new_b + 'x'
            counter += 1
            if counter > 1:
                return None
        else:
            new_b = new_b + b1[i]
    return new_b

def look_for_matched_pairs(group:dict,size:int)->dict:
    pairs = {}
    for i in range(1,size+1):
        if (i in group) and ((i-1) in group):
            pairs[i-1] = []
            for row in group[i-1]:
                for b in group[i]:
                    r = compare_and_chage(row[-1],b[-1])
                    if r != None:
                        pairs[i-1].append([row[0] + b[0],True,r])
                        row[1] = False
                        b[1] = False
            if len(pairs[i-1]) == 0:
                del pairs[i-1]
    return pairs

def look_for_prime_implicants(lists:list)->list:
    prime_implicants = []
    prime_implicants_hashes = set()
    for dic in lists:
        for lv in dic.values():
            for value in lv:
                if value[1] and (value[-1] not in prime_implicants_hashes):
                    prime_implicants.append([value[-1],value[0]])
                    prime_implicants_hashes.add(value[-1])
    return prime_implicants

def prime_implicant_table(prime_implicants:list,minterms:list)->dict:
    table = {}
    for minterm in minterms:
        table[minterm] = []
        for prime_implicant in prime_implicants:
            if minterm in prime_implicant[-1]:
                table[minterm].append(prime_implicant[0])
    return table


def assign_letters_to_minterm(bin_minterm:str)->str:
    str_minterm = ""
    for i in range(0,len(bin_minterm)):
        if bin_minterm[i] == '0':
            str_minterm = str_minterm + chr(65 + i) + "'"
        elif bin_minterm[i] == '1':
            str_minterm = str_minterm + chr(65 + i)
    return str_minterm

def create_function(minterms:list)->str:
    final_function = ""
    for minterm in minterms:
        final_function += assign_letters_to_minterm(minterm)
        if minterm != minterms[-1]:
            final_function += " + "
    return final_function

def create_sets(prime_implicants:list)->dict:
    prime_implicant_table = {}
    for prime_implicant in prime_implicants:
        prime_implicant_table[prime_implicant[0]] = set(prime_implicant[1])
    return prime_implicant_table

def look_for_epis(prime_implicants:dict)->set:
    #####looking for essential prime implicants
    epis = set()
    for key in prime_implicants:
        prime_implicant_set = prime_implicants[key]
        for another_key in prime_implicants:
            if key != another_key:
                prime_implicant_set = prime_implicant_set - prime_implicants[another_key]
                if not prime_implicant_set:
                    break
        if prime_implicant_set:
            epis.add(key)
    return epis

def delete_epis_from_table(epis:set,prime_implicants:dict)->None:
    covered_mintermns = set()
    #####Getting mintermns that ara already covered by the EPIs
    for key in epis:
        covered_mintermns = covered_mintermns | prime_implicants[key]
        #####Deleting EPIs from table
        del prime_implicants[key]
    #####Deleting mintermns that are already covered
    empty_epis = []
    for key in prime_implicants:
        prime_implicant_set = prime_implicants[key]
        prime_implicant_set = prime_implicant_set - covered_mintermns
        prime_implicants[key] = prime_implicant_set
        if not prime_implicant_set:
            empty_epis.append(key)
    #####Deleting for empty EPIs
    for empty_epi in empty_epis:
        del prime_implicants[empty_epi]

def column_dominance(prime_implicants:dict)->dict:
    dominant_prime_implicants = set()
    #####looking for dominant prime implicants
    for key in prime_implicants:
        if key not in dominant_prime_implicants:
            dpi = key
            for another_key in prime_implicants:
                if key != another_key and prime_implicants[another_key]:
                    aux_set = prime_implicants[dpi] - prime_implicants[another_key]
                    if not aux_set:
                        dpi = another_key
                    elif (prime_implicants[dpi] == prime_implicants[another_key]) and (dpi.count('x') < another_key.count('x')):
                        dpi = another_key
            if dpi not in dominant_prime_implicants:
                dominant_prime_implicants.add(dpi)
    #####Deleting non dominant prime implicants
    non_dominant_prime_implicants = set(prime_implicants.keys()) - dominant_prime_implicants
    for key in list(prime_implicants.keys()):
        if key in non_dominant_prime_implicants:
            del prime_implicants[key]
        
    return prime_implicants

def quine_mcCluskey(minterms:list,size:int)->str:
    rows = [int_to_str_bin(minterm,size) for minterm in minterms]
    first_group = group_rows(rows)
    lists = [first_group]

    pairs = look_for_matched_pairs(first_group,size)
    while len(pairs) > 0:
        lists.append(pairs)
        pairs = look_for_matched_pairs(pairs,size)

    prime_implicants = look_for_prime_implicants(lists)
    #####Reducing prime implicant chart
    pis_sets = create_sets(prime_implicants)
    epis = set()
    while len(pis_sets) > 0:
        print(pis_sets)
        new_epis = look_for_epis(pis_sets)
        delete_epis_from_table(new_epis,pis_sets)
        epis = epis | new_epis
        pis_sets = column_dominance(pis_sets)
        pis_sets = column_dominance(pis_sets)

    logic_function = create_function(list(epis))
    return logic_function

if __name__ == '__main__':
    result = quine_mcCluskey([0,2,3,4,6],3)
    print(result)
    result =  quine_mcCluskey([0,1,2,4,6,10,12,13,16,20,21,23,25,26,27,28,30,31],5)
    print(result)
    result =  quine_mcCluskey([0, 2, 5, 6, 7, 8, 10, 12, 13, 14, 15],4)
    print(result)
    result =  quine_mcCluskey([0, 2, 3,7,9,11,12,14,15],4)
    print(result)