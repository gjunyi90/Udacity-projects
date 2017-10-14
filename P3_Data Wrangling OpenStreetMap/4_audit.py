"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from optparse import OptionParser
import collections



OSMFILE = "sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
zip_re = re.compile(r'NE[^\s]\w{3,5}', re.IGNORECASE)
zip_re2 = re.compile(r'NE[^\s]\w{3}', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd": "Road",
            "Dr": "Drive",
            "Aenue": "Avenue"
            }
##################################################################################
################################# Street Types ###################################
##################################################################################
            
### Auditing Street Types
def audit_street_type(street_types, street_name): # only if it is elem.attrib['k'] == "addr:street")
    # Function will check for expected suffix for streetnames
    # If it is not expected, the detected suffix will be stored
    m = street_type_re.search(street_name)
    if m: # if (it matches regex)
        street_type = m.group() # Returns one or more subgroups of the match
        if street_type not in expected:
            street_types[street_type].add(street_name) # street_name is the raw street name
            #print street_types

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    # Iterate in the xml file to replace non-standardized street names
    osm_file = open(OSMFILE, "r")
    street_types = defaultdict(set)
    auditted = ET.parse(osm_file)
    auditlist = list(auditted.iter())
    street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
    for elem in auditlist:
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    if audit_street_type(street_types, tag.attrib['v']):
                        #Update the tag attribtue
                        tag.attrib['v'] = update_name(tag.attrib['v'],mapping,street_type_re)
    #write the to the file we've been audit
    auditted.write('audit.osm')
    return street_types
def update_name(st_types2, mapping, street_type_re): 
    # Updates the street type that is detected replace with correct one from mapping dictionary
    re_search = street_type_re.search(st_types2)
    if re_search:
        detected = re_search.group() #This method returns all matching subgroups in a tuple 
        if detected in mapping:
            st_types2 = re.sub(street_type_re, mapping[detected], st_types2)
    return st_types2

##################################################################################
################################# Postal Codes ###################################
##################################################################################

def audit_zipcode(invalid_zipcodes, zipcode):
    # Function will look for wrong format postal codes
    # Prints out the old and the new format
    m = zip_re.search(zipcode)
    if m: # if (it matches regex)
        zipsearch = m.group() # Returns one or more subgroups of the match
        zipsearch2 = update_zip(zipsearch)
        print zipsearch, "=>", zipsearch2
        
def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")
    
def audit_zip(osmfile):
    # Iterate in the xml file to replace non-standardized street names
    osm_file = open("audit.osm", "r")
    zips = defaultdict(set)
    auditted_zips = ET.parse(osm_file)
    auditlist_zip = list(auditted_zips.iter())
    for elem in auditlist_zip:
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    oldkey = tag.attrib['k']
                    tag.attrib['k'] = "addr:postcode" # Standadizes the key name for postcodes
                    newkey = tag.attrib['k']
                    """ # Uncomment the above to print out the corrected keys
                    if oldkey != newkey:
                        print oldkey, "(Old Key)=>", newkey, '(New Key)'
                    """
                    if audit_zipcode(zips, tag.attrib['v']):
                        #Update the tag attribtue
                        tag.attrib['v'] = update_zip(tag.attrib['v'])
                        
    auditted_zips.write('audit.osm')
    return zips    
    
def update_zip(zipsearch):
    audited_zip = re.sub(r"(\w{3})$", r" \1", zipsearch)
    return audited_zip

##########################################################################
################################# Main ###################################
##########################################################################

def test():
    st_types = audit(OSMFILE) #in the audit(), it returns street_types; st_types=street_types

    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(st_type, mapping, street_type_re)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"
                
    sf_zipcode = audit_zip(OSMFILE)
    pprint.pprint(dict(sf_zipcode))

if __name__ == '__main__':
    test()
    parser  = OptionParser()
    parser.add_option('-d', '--data', dest='audited_data', help='osm data that want to be audited')
    (opts,args) = parser.parse_args()
    audit(opts.audited_data)