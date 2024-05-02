
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
            #print(lv)
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

def simplification(table:dict)->set:
    selected_prime_implicants = set()
    while len(table) > 1:
        #-----loking for prime implicants that cover one minterm only
        for minterm in table:
            if len(table[minterm]) == 1:
                selected_prime_implicants.add(table[minterm][0])
        #-----deleting columns that are alredy covered by selected prime implicants
        for selected in selected_prime_implicants:
            keys = list(table.keys())
            for minterm in keys:
                if selected in table[minterm]:
                    del table[minterm]
        #-----looking for prime implicants that appear once but if the table has more than one column only
        if len(table) > 1:
            once_prime_impliants = []
            more_than_once_prime_impliants = set()
            for minterm in table:
                for prime_implicant in table[minterm]:
                    if (prime_implicant not in once_prime_impliants) and (prime_implicant not in more_than_once_prime_impliants):
                        once_prime_impliants.append(prime_implicant)
                    elif (prime_implicant in once_prime_impliants):
                        once_prime_impliants.remove(prime_implicant)
                        more_than_once_prime_impliants.add(prime_implicant)
            #-----Deleting prime implicants that appear once
            for minterm in table:
                for bad_prime_implicant in once_prime_impliants:
                    if bad_prime_implicant in table[minterm]:
                        table[minterm].remove(bad_prime_implicant)
        elif len(table) == 1:
            #-----Looking for the best prime implicant for the left column
            minterm = list(table.keys())[0]
            prime_implicants = table[minterm]
            best_option = prime_implicants[0]
            for prime_implicant in prime_implicants[1:]:
                if best_option.count('x') < prime_implicant.count('x'):
                    best_option = prime_implicant
            selected_prime_implicants.add(best_option)
            del table[minterm]
    
    return selected_prime_implicants

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
    print('original table')
    print(table)
    print('unique prime implicants')
    x = simplification(table)
    print(create_function(list(x)))
    print('leftovers')
    print(table)

if __name__ == '__main__':
    quine_mcCluskey([0,2,3,4,6],3)
    quine_mcCluskey([0,1,2,4,6,10,12,13,16,20,21,23,25,26,27,28,30,31],5)