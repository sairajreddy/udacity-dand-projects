import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

tomap = {
           "Blr": "Bengaluru",
           "bangalore": "Bengaluru",
           "Bangalore": "Bengaluru",
           "nagar": "Nagar",
           "Ngr": "Nagar",
           "Rd.": "Road",
           "road": "Road",
           "Rd,": "Road,",
           "road,": "Road,",
           "road": "Road",
           "Rd": "Road",
           "layout,": "Layout,",
           "layout": "Layout",
           "main": "Main Road",
           "main rd.": "Main Road",
           "Main": "Main Road",
           "Main Road": "Main Road",
        }
        
exp = ["Bengaluru", "Colony", "Layout", "Road", "Nagar", "Main Road"]

data = "data/bengaluru_india.osm"
reg = re.compile(r'\b\S+\.?', re.IGNORECASE)

def street_audit(street_type, street_name): 
    match = reg.search(street_name)
    if match:
        street_t = match.group()
        if street_t not in exp:
            street_type[street_t].add(street_name)

def street_audit_2(street_name): 
    match = reg.search(street_name)
    if match:
        street_type = match.group()
        if street_type not in exp:
            return True; return False

def is_street_name(e): 
    return (e.attrib['k'] == "addr:street")

def audit(osmfile): 
    osm_file = open(osmfile, "r")
    street_type = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    street_audit(street_type, tag.attrib['v'])

    return street_type


def convert_case(string): 
    if string.isupper():
        return string
    else:
        return string.title()


def name_update(n, tm):
    n = n.split(' ')
    for i in range(len(n)):
        if n[i] in tm:
            n[i] = tm[n[i]]
            n[i] = convert_case(n[i])
        else:
            n[i] = convert_case(n[i])
    
    n = ' '.join(n)
    return n

update_street = audit(data) 