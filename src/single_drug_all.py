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


# generate query url using given input parameters
#def query(drug_name):

# generate JSON dictionary using given input parameters
def query(drug_name):
    
# generate JSON dictionary using given input parameters
def query(drug_name, limit):

     prefix = "https://api.fda.gov/drug/event.json?api_key=vZC1Gh1XyJl58wZKsMfJifZisDOFRsGBCij3G32v&search=patient.drug.openfda.brand_name:"
     q = "%22"
    return prefix + q + drug_name + q + "w"
    
    URL = prefix + q + drug_name + q + '&limit=' + str(limit)
    print URL
    j = urllib2.urlopen(URL)
    d = json.load(j)
    return d
 
 #---------------------------------------------------------#
 

 # store command line argument (string for drug name)
 #drug_name = 'Lipitor'
 #sys.argv[1] = 'Lipitor'
@@ -32,6 +43,25 @@ def query(drug_name):
 # j = urllib2.urlopen(URL)
 # data = json.load(j)
 # print(data)

# query user for the input (string for drug name)
drug_name = raw_input("Drug name?: ")
limit = 1
init = query(drug_name, limit)

# total # of records for that drug
total = init['meta']['results']['total'] 

# find the # of records associated with the age, weight, sex
sex = raw_input("Sex (Input : ")
# need to set the limit on the query = total # of records
# can only query 100 records at a time, so need to divide by 100 and query that many times
data = query(drug_name, total)
print len(data['results'])


 # process data
 '''
analyze data here