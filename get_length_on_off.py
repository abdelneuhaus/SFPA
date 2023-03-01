def get_length_on(random_list):
    retlist = []
    count = 1
    i = 1
    while i < len(random_list):
        if random_list[i] == random_list[i-1] + 1:
            count += 1
        else:
            retlist.append(count)
            count = 1
        i += 1
    retlist.append(count)
    return retlist


def get_length_off(random_list):
    sorted_lst = sorted(random_list)
    retlist = []
    count = 0
    for i in range(1, len(sorted_lst)):
        if sorted_lst[i] - sorted_lst[i-1] > 1:
            count = sorted_lst[i] - sorted_lst[i-1] - 1
            retlist.append(count)
    return retlist

a = [1,2,4,9,10]
print(get_length_on(a))
print(get_length_off(a)) # doit donner 1, 4