
def int_to_str_bin(number:int,size:int)->str:
    return format(number,f'0{size}b')

def bits_on(str_bin:str)->int:
    return str_bin.count('1')

def group_rows(rows:list)->dict:
    group = {}
    for row in rows:
        b_on = bits_on(row)
        if b_on in group:
            group[b_on].append(row)
        else:
            group[b_on] = [row]
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

def look_for_matched_pairs(group:dict,size:int):
    pairs = {}
    for i in range(1,size+1):
        if (i in group) and ((i-1) in group):
            pairs[i-1] = []
            for row in group[i-1]:
                for b in group[i]:
                    r = compare_and_chage(row,b)
                    if r != None:
                        pairs[i-1].append((row,b,r))
    return pairs


def quine_mcCluskey(minterms:list,size:int):
    rows = [int_to_str_bin(minterm,size) for minterm in minterms]
    first_group = group_rows(rows)
    print(first_group)
    pairs = look_for_matched_pairs(first_group,size)
    print(pairs)


quine_mcCluskey([5,12,16,19,20,2,13,0],5)
print(compare_and_chage('x00','x10'))