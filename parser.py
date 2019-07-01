import re
from CaseInsensitiveDict import CaseInsensitiveDict
import pandas as pd

_suffix_csv = pd.read_csv('./suffix.csv')
_dir_csv = pd.read_csv('./directions.csv')
_suffix_dict = _suffix_csv.set_index('input')['output'].to_dict()
_suffix_i = CaseInsensitiveDict(_suffix_dict)
_dir_dict = _dir_csv.set_index('input')['output'].to_dict()
_dir_i = CaseInsensitiveDict(_dir_dict)
def _replace_suffix(m):
    return _suffix_i.get(m.group('key'), m.group(0))
def _replace_dir(m):
    return _dir_i.get(m.group('key'), m.group(0))


_regexp_unit_suite = r'(?i)(SUITE|STE|UNIT|APT)s? \S+'
_regexp_hash = r'#\S+'
# note: stdlib.re doesn't work with \p{P} for punct
# thanks to https://stackoverflow.com/questions/56161249/delete-all-punctuation-symbols-exept-underscore-and-curly-braces-in-string-in-py
_regexp_remove_punct_keep_hyphon = r'[^\w -]|(?<![\d])-|-(?![\d])'
_regexp = r'|'.join((_regexp_unit_suite, _regexp_hash, _regexp_remove_punct_keep_hyphon))
_regexp_extra_space = r' +' 


def parse_building_address(addr_string):
    """ parse and standardize address field to street number, street name ONLY, removing suite/unit/ number 
    """
    addr_string = re.sub(_regexp, '', addr_string)
    addr_string = re.sub(r'(?P<key>[a-zA-Z]+)', _replace_dir, addr_string)
    addr_string = re.sub(r'(?P<key>[a-zA-Z]+)', _replace_suffix, addr_string)
    addr_string = re.sub(_regexp_extra_space, ' ', addr_string)
    return addr_string.strip().upper()