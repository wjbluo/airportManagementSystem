def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def is_all_number_Matrix(dic):
    try:
        flag = True
        for item in dic:
            if not is_number(item):
                flag = False
    except (TypeError, ValueError):
        pass
    return flag

