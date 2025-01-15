import re


def clean(s):
    log_format = re.sub(r'[0-9A-Za-z, ]+', '', s)
    unique_chars = list(set(log_format))
    sorted_string = ''.join(sorted(unique_chars))
    s = re.sub(r':|\(|\)|=|,|"|\{|\}|@|$|\[|\]|\||;|\.?!', ' ', s)
    s = " ".join([word for word in s.strip().split()
                 if not bool(re.search(r'\d', word))])
    # trantab = str.maketrans(dict.fromkeys(list(string.punctuation)))
    return s, sorted_string
