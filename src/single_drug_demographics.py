'''
Load all records associated with a single drug
Call in command line as follows: python single-drug-demographics.py DRUGNAME
Matthew Mallick
April 7, 2015
'''

# import module for opening URLs
import urllib2
# import module for working with JSON files
import json
# import module for command line arguments
import sys

#---------------------------------------------------------#

# generate query url using given input parameters
def query_count(drug_name):
    prefix = "https://api.fda.gov/drug/event.json?api_key=vZC1Gh1XyJl58wZKsMfJifZisDOFRsGBCij3G32v&search=patient.drug.openfda.brand_name:"
    q = "%22"
    suffix = "&count=patient.reaction.reactionmeddrapt.exact"
    return prefix + q + drug_name + q + suffix

#---------------------------------------------------------#

# store command line argument (string for drug name)
drug_name = sys.argv[1]
# load query result in json format
URL = query_count(drug_name)
j = urllib2.urlopen(URL)
data = json.load(j)
# process data
'''
analyze data here
'''