# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 21:38:46 2016

@author: Jun
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
tryingjun = re.compile(r'[jun]')

def key_type(element, keys):
    if element.tag == "tag":
        print element.attrib['k']
        
        if lower.match(element.attrib['k']) != None:
            keys['lower'] += 1
        elif lower_colon.match(element.attrib['k']) != None:
            keys['lower_colon'] += 1
        elif problemchars.match(element.attrib['k']) != None:
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
        
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    keys = process_map('example.osm')
    pprint.pprint(keys)
    #assert keys == {'lower': 5, 'tryingjun': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()