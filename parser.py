import re
from CaseInsensitiveDict import CaseInsensitiveDict
import pandas as pd

line = "-Unit #203-B,  300-499,   North State STREET Boulevard Avenue @chicaog, ste 3210b"
regexp_unit_suite = r'(?i)(SUITE|STE|UNIT|APT)s? \S+'
regexp_hash = r'#\S+'
# note: stdlib.re doesn't work with \p{P} for punct
# thanks to https://stackoverflow.com/questions/56161249/delete-all-punctuation-symbols-exept-underscore-and-curly-braces-in-string-in-py
regexp_remove_punct_keep_hyphon = r'[^\w -]|(?<![\d])-|-(?![\d])'
regexp = r'|'.join((regexp_unit_suite, regexp_hash, regexp_remove_punct_keep_hyphon))

line = re.sub(regexp, '', line)
repeated_space = r' +' 
line = re.sub(repeated_space, ' ', line)

# remove leading and trailing white spaces
line = line.strip() 

suffix_csv = pd.read_csv('./suffix.csv')
suffix_dict = suffix_csv.set_index('input')['output'].to_dict()
suffix_i = CaseInsensitiveDict(suffix_dict)

def replace_it(m):
    return suffix_i.get(m.group('key'), m.group(0))

line = re.sub(r'(?P<key>[a-zA-Z]+)', replace_it, line)
print(line)
