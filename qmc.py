
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
            print(lv)
            for value in lv:
                if value[1] and (value[-1] not in prime_implicants_hashes):
                    prime_implicants.append([value[-1],value[0]])
                    prime_implicants_hashes.add(value[-1])
    return prime_implicants

def prime_implicant_table(prime_implicants:list,minterms:list)->dir:
    table = {}
    for minterm in minterms:
        table[minterm] = []
        for prime_implicant in prime_implicants:
            if minterm in prime_implicant[-1]:
                table[minterm].append(prime_implicant[0])
    return table


def quine_mcCluskey(minterms:list,size:int):
    rows = [int_to_str_bin(minterm,size) for minterm in minterms]
    first_group = group_rows(rows)
    lists = [first_group]

    pairs = look_for_matched_pairs(first_group,size)
    while len(pairs) > 0:
        lists.append(pairs)
        pairs = look_for_matched_pairs(pairs,size)

    prime_implicants = look_for_prime_implicants(lists)
    table = prime_implicant_table(prime_implicants,rows)
    print(table)

#quine_mcCluskey([5,12,16,19,20,2,13,0],5)
quine_mcCluskey([0,2,3,4,6],3)