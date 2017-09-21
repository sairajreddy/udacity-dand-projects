import xml.etree.cElementTree as ET
import re
import csv
import codecs
import cerberus
from unittest import TestCase

import a_audit_data 
import c_create_schema

lower_case_colon = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
problematic = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

OSM_PATH = "data/bengaluru_india.osm"
NODE_TAGS_PATH = "data/bi_nodes_tags.csv"
NODES_PATH = "data/bi_nodes.csv"
WAYS_PATH = "data/bi_ways.csv"
WAY_TAGS_PATH = "data/bi_ways_tags.csv"
WAY_NODES_PATH = "data/bi_ways_nodes.csv"

SCHEMA = c_create_schema.schema

node_fields = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
node_tag_fields = ['id', 'key', 'value', 'type']

bi_way_fields = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
bi_way_tag_fields = ['id', 'key', 'value', 'type']
bi_way_node_fields = ['id', 'node_id', 'position']


def shape(elem, node_attr_fields=node_fields, way_attr_fields=bi_way_fields,
                  problem_chars=problematic, default_tag_type='regular'):

    n_attributes = {}
    w_attributes = {}
    tags = []
    w_nodes = []
    
    if elem.tag == 'node':
        for attrib in elem.attrib:
            if attrib in node_fields:
                n_attributes[attrib] = elem.attrib[attrib]
        
        for child in elem:
            node_tag = {}
            if lower_case_colon.match(child.attrib['k']):
                node_tag['type'] = child.attrib['k'].split(':',1)[0]
                node_tag['key'] = child.attrib[ 'k'].split(':',1)[1]
                node_tag['id'] = elem.attrib['id']
                if child.attrib['k']=="addr:street" and a_audit_data.street_audit_2( child.attrib['k']):
                    node_tag['value'] = a_audit_data.name_update(child.attrib['v'], a_audit_data.tomap)
                else:
                    node_tag['value'] = child.attrib['v']
                tags.append(node_tag)
            elif problematic.match(child.attrib['k']):
                continue
            else:
                node_tag['type'] = 'regular'
                node_tag['key'] = child.attrib['k']
                node_tag['id'] = elem.attrib['id']
                if child.attrib['k']=="addr:street" and a_audit_data.street_audit_2( child.attrib['k']):
                    node_tag['value'] = a_audit_data.name_update(child.attrib['v'], a_audit_data.tomap)
                else:
                    node_tag['value'] = child.attrib['v']
                tags.append(node_tag)
        
        return {'node': n_attributes, 'node_tags': tags}
        
    elif elem.tag == 'way':
        for attrib in elem.attrib:
            if attrib in bi_way_fields:
                w_attributes[attrib] = elem.attrib[attrib]
        
        position = 0
        for child in elem:
            way_tag = {}
            way_node = {}
            
            if child.tag == 'tag':
                if lower_case_colon.match(child.attrib['k']):
                    way_tag['type'] = child.attrib['k'].split(':',1)[0]
                    way_tag['key'] = child.attrib['k'].split(':',1)[1]
                    way_tag['id'] = elem.attrib['id']
                    if child.attrib['k']=="addr:street" and a_audit_data.street_audit_2( child.attrib['k']):
                        way_tag['value'] = a_audit_data.name_update(child.attrib['v'], a_audit_data.tomap)
                    else:
                        way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
                elif problematic.match(child.attrib['k']):
                    continue
                else:
                    way_tag['type'] = 'regular'
                    way_tag['key'] = child.attrib['k']
                    way_tag['id'] = elem.attrib['id']
                    if child.attrib['k']=="addr:street" and a_audit_data.street_audit_2( child.attrib['k']):
                        way_tag['value'] = a_audit_data.name_update(child.attrib['v'], a_audit_data.tomap)
                    else:
                        way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
                    
            elif child.tag == 'nd':
                way_node['id'] = elem.attrib['id']
                way_node['node_id'] = child.attrib['ref']
                way_node['position'] = position
                position += 1
                w_nodes.append(way_node)
        
        return {'way': w_attributes, 'w_nodes': w_nodes, 'way_tags': tags}



def get(osm_file, tags=('node', 'way', 'relation')):

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_ele(elem, validator, schema=SCHEMA):

    if validator.validate(elem, schema) is not True:
        field, errors = next(iter(validator.errors.items()))
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.items()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in list(row.items())
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)



def process(file_in, validate):
    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, node_fields)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, node_tag_fields)
        ways_writer = UnicodeDictWriter(ways_file, bi_way_fields)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, bi_way_node_fields)
        way_tags_writer = UnicodeDictWriter(way_tags_file, bi_way_tag_fields)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for elem in get(file_in, tags=('node', 'way')):
            el = shape(elem)
            if el:
                if validate is True:
                    validate_ele(el, validator)

                if elem.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif elem.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['w_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    process(OSM_PATH, validate=True)