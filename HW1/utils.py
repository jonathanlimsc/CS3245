import re

def normalize(raw_str, casefold=True, sym_num=True):
    '''
    Normalizes a raw_str by case folding and removing symbols and numbers.
    By default, case folding and removal of numbers will occur.

    Returns the normalized string.
    '''
    processed_str = raw_str
    if casefold:
        processed_str = processed_str.lower()
    if sym_num:
        processed_str = re.sub(r'[^a-zA-Z\s+]+', '', processed_str)
    # Strip multiple spaces to single space
    ' '.join(processed_str.split())

    return processed_str

def tokenize(input_str, n=4):
    '''
    Tokenizes input_str into substrings of length n. The tokenizing window moves down
    input_str one character at a time.

    Returns an array of tokens.
    '''
    return [input_str[base_idx:base_idx+n] for base_idx in range(0, len(input_str)-n+1)]

if __name__ == '__main__':
    test_str = "Tapak-tapak berhampiran yang dimiliki oleh syarikat yang sama atau yang ditebus guna, diratakan atau diisi dengan tanah juga boleh mengalami pencemaran walaupun guna tanah terkini kelihatan tidak berbahaya."
    test_str2 = "Seandainya Allah tidak campur tangan, Iblis dan manusia di dalam dosa akan bersekutu melawan surga, dan gantinya bermusuhan melawan Setan, segenap manusia akan bersatu melawan Allah."
    processed = normalize(test_str)
    processed2 = normalize(test_str2)
    tokenize(processed)
    tokenize(processed2)
