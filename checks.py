def pr_valid(files_list, ignore_list):
    ignore = 0
    for item in files_list:
        if any(x in item.filename for x in ignore_list):
            ignore+=1
    
    if files_list.totalCount == ignore:
        return False
    else:
        return True

def look_for_tests(files_list, test_patterns):
    for item in files_list:
        if any(x in item.filename for x in test_patterns):
            return True
    return False