'''
Load all records associated with a single drug
Call in command line as follows: python single-drug-all.py DRUGNAME
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

# generate JSON dictionary using given input parameters
def query(drug_name, limit):
    prefix = "https://api.fda.gov/drug/event.json?api_key=vZC1Gh1XyJl58wZKsMfJifZisDOFRsGBCij3G32v&search=patient.drug.openfda.brand_name:"
    q = "%22"
    
    URL = prefix + q + drug_name + q + '&limit=' + str(limit)
    j = urllib2.urlopen(URL)
    d = json.load(j)
    return d

#---------------------------------------------------------#

# store command line argument (string for drug name)
drug_name = sys.argv[1]

limit = 1
init = query(drug_name, limit)

# total # of records for that drug
total = init['meta']['results']['total'] 





# need to set the limit on the query 

# process data
'''
analyze data here
'''