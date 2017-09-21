import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import csv

lower_case = re.compile(r'^([a-z]|_)*$')
problematic = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
left_case_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')

data = "data/bengaluru_india.osm"

def key(ele, keys):
    if ele.tag == "tag":
        for tag in ele.iter('tag'):
            k = tag.get('k')
            if lower_case.search(ele.attrib['k']):
                keys['lower_case'] = keys['lower_case'] + 1
            elif left_case_colon.search(ele.attrib['k']):
                keys['left_case_colon'] = keys['left_case_colon'] + 1
            elif problematic.search(ele.attrib['k']):
                keys['problematic'] = keys['problematic'] + 1
            else:
                keys['other'] = keys['other'] + 1
    return keys


def map(filename):
    keys = {"lower_case": 0, "left_case_colon": 0, "problematic": 0, "oth": 0}
    for _, ele in ET.iterparse(filename):
        keys = key(ele, keys)
    return keys

pprint.pprint(map(data))
