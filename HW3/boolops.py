def list_and(list1, list2):
    '''
    Takes two lists and iteratively merges them.
    Returns a list of doc ids that are present in both lists.
    '''
    doc_ids = []
    len1 = len(list1)
    len2 = len(list2)
    idx_1 = 0
    idx_2 = 0

    while idx_1 < len1 and idx_2 < len2:
        if list1[idx_1] == list2[idx_2]:
            doc_ids.append(list1[idx_1])
            idx_1 += 1
            idx_2 += 1
        elif list1[idx_1] < list2[idx_2]:
            idx_1 += 1
        elif list1[idx_1] > list2[idx_2]:
            idx_2 += 1

    return doc_ids

def list_or(list1, list2):
    '''
    Takes two lists.
    Returns doc ids that appear in either list.
    '''
    doc_ids = []
    len1 = len(list1)
    len2 = len(list2)
    idx_1 = 0
    idx_2 = 0

    while idx_1 < len1 and idx_2 < len2:
        if list1[idx_1] < list2[idx_2]:
            doc_ids.append(list1[idx_1])
            idx_1 += 1
        elif list1[idx_1] > list2[idx_2]:
            doc_ids.append(list2[idx_2])
            idx_2 += 1
        elif list1[idx_1] == list2[idx_2]:
            doc_ids.append(list1[idx_1])
            idx_1 += 1
            idx_2 += 1

    if idx_1 < len1:
        doc_ids.extend(list1[idx_1:])
    if idx_2 < len2:
        doc_ids.extend(list2[idx_2:])

    return doc_ids

# TODO: For future optimisation
def list_and_not(list1, list2):
    '''
    Takes two lists.
    Returns a list of doc ids that are present in list a and not list b.
    Ie. removes anything in list1 that appears in list2
    '''
    doc_ids = []
    len1 = len(list1)
    len2 = len(list2)
    idx_1 = 0
    idx_2 = 0

    while idx_1 < len1 and idx_2 < len2:
        if list1[idx_1] < list2[idx_2]:
            doc_ids.append(list1[idx_1])
            idx_1 += 1
        elif list1[idx_1] > list2[idx_2]:
            idx_2 += 1
        elif list1[idx_1] == list2[idx_2]:
            idx_1 += 1
            idx_2 += 1

    if idx_1 < len1:
        doc_ids.extend(list1[idx_1:])

    return doc_ids

def plist_and(p1, p2, p_file):
    '''
    Takes the starting entries of two posting lists and the posting file and iteratively merges
    the two lists.
    Returns the doc ids that are present in both lists.
    '''
    doc_ids = []
    while p1 != None and p2 != None:
        if p1.doc_id == p2.doc_id:
            doc_ids.append(p1.doc_id)
            p1 = p_file.get_next_entry(p1)
            p2 = p_file.get_next_entry(p2)
        elif p1.doc_id < p2.doc_id:
                p1 = p_file.get_next_entry(p1)
        elif p1.doc_id > p2.doc_id:
                p2 = p_file.get_next_entry(p2)

    return doc_ids

def plist_or(p1, p2, p_file):
    '''
    Takes the starting entries of two posting lists and the posting file.
    Returns the doc ids that are present in either list.
    '''
    doc_ids = []

    while p1 != None and p2 != None:
        if p1.doc_id == p2.doc_id:
            doc_ids.append(p1.doc_id)
            p1 = p_file.get_next_entry(p1)
            p2 = p_file.get_next_entry(p2)
        elif p1.doc_id < p2.doc_id:
            doc_ids.append(p1.doc_id)
            p1 = p_file.get_next_entry(p1)
        elif p1.doc_id > p2.doc_id:
            doc_ids.append(p2.doc_id)
            p2 = p_file.get_next_entry(p2)

    if p1 != None:
        while p1 != None:
            doc_ids.append(p1.doc_id)
            p1 = p_file.get_next_entry(p1)
    if p2 != None:
        while p2 != None:
            doc_ids.append(p2.doc_id)
            p2 = p_file.get_next_entry(p2)

    return doc_ids

def plist_list_and(p, list, p_file):
    '''
    Takes the starting entry of a posting list, a list and a posting file.
    Returns the doc ids that appear in both the posting list and list.
    '''
    doc_ids = []
    idx = 0
    list_len = len(list)

    while p != None and idx < list_len:
        if p.doc_id == list[idx]:
            doc_ids.append(p.doc_id)
            p = p_file.get_next_entry(p)
            idx += 1
        elif p.doc_id < list[idx]:
            p = p_file.get_next_entry(p)
        elif p.doc_id > list[idx]:
            idx += 1

    return doc_ids

def plist_list_or(p, list, p_file):
    '''
    Takes the starting entry of a posting list, a list and a posting file.
    Returns the doc ids that appear in either the posting list and list.
    '''
    doc_ids = []
    idx = 0
    list_len = len(list)

    while p != None and idx < list_len:
        if p.doc_id == list[idx]:
            doc_ids.append(p.doc_id)
            p = p_file.get_next_entry(p)
            idx += 1
        elif p.doc_id < list[idx]:
            doc_ids.append(p.doc_id)
            p = p_file.get_next_entry(p)
        elif p.doc_id > list[idx]:
            doc_ids.append(p.doc_id)
            idx += 1

    if p != None:
        while p != None:
            doc_ids.append(p.doc_id)
            p = p_file.get_next_entry(p)
    if idx < list_len:
        doc_ids.extend(list[idx:])

    return doc_ids

def plist_not(p, all_ids, p_file):
    '''
    Returns all the doc_ids of the documents that are not in the
    p_list.
    '''
    p_ids = set()
    print "plist_not"
    while p != None:
        p_ids.add(p.doc_id)
        p = p_file.get_next_entry(p)

    return list(all_ids - p_ids)

# print list_or([1,3,6,7,8], [2,3,4,5,6,10,12])
# print list_and([1,3,6,7,8], [2,3,4,5,6,10,12])
# print list_and_not([1,3,6,7,8], [2,3,4,5,6,10,12])
