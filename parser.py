import re
from CaseInsensitiveDict import CaseInsensitiveDict
import pandas as pd

suffix_csv = pd.read_csv('./suffix.csv')
dir_csv = pd.read_csv('./directions.csv')
suffix_dict = suffix_csv.set_index('input')['output'].to_dict()
suffix_i = CaseInsensitiveDict(suffix_dict)
dir_dict = dir_csv.set_index('input')['output'].to_dict()
dir_i = CaseInsensitiveDict(dir_dict)
def replace_suffix(m):
    return suffix_i.get(m.group('key'), m.group(0))
def replace_dir(m):
    return dir_i.get(m.group('key'), m.group(0))


regexp_unit_suite = r'(?i)(SUITE|STE|UNIT|APT)s? \S+'
regexp_hash = r'#\S+'
# note: stdlib.re doesn't work with \p{P} for punct
# thanks to https://stackoverflow.com/questions/56161249/delete-all-punctuation-symbols-exept-underscore-and-curly-braces-in-string-in-py
regexp_remove_punct_keep_hyphon = r'[^\w -]|(?<![\d])-|-(?![\d])'
regexp = r'|'.join((regexp_unit_suite, regexp_hash, regexp_remove_punct_keep_hyphon))
regexp_extra_space = r' +' 

line = "-Unit #203-B,  300-499,   North State STREET Boulevard S @chicago, ste 3210b"
line = re.sub(regexp, '', line)
line = re.sub(r'(?P<key>[a-zA-Z]+)', replace_dir, line)
line = re.sub(r'(?P<key>[a-zA-Z]+)', replace_suffix, line)
line = re.sub(regexp_extra_space, ' ', line)

# remove leading and trailing white spaces
line = line.strip() 


print(line)
