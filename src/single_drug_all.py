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
# import module numpy for matrices
import numpy
from bundlebuilder import SUFFIXES
import operator

#---------------------------------------------------------#
# generates a JSON library with the counts
def query_count(drug_name):
    prefix = "https://api.fda.gov/drug/event.json?api_key=vZC1Gh1XyJl58wZKsMfJifZisDOFRsGBCij3G32v&search=patient.drug.openfda.brand_name:"
    q = "%22"
    suffix = "&count=patient.reaction.reactionmeddrapt.exact"
    URL = prefix + q + drug_name + q + suffix
    print URL
    j = urllib2.urlopen(URL)
    d = json.load(j)
    return d

#---------------------------------------------------------#

# generate JSON dictionary using given input parameters
def query_drug(drug_name, limit):
    prefix = "https://api.fda.gov/drug/event.json?api_key=vZC1Gh1XyJl58wZKsMfJifZisDOFRsGBCij3G32v&search=patient.drug.openfda.brand_name:"
    q = "%22"
    
    URL = prefix + q + drug_name + q + '&limit=' + str(limit)
    #print URL
    j = urllib2.urlopen(URL)
    d = json.load(j)
    return d

#---------------------------------------------------------#

# generate query url for counts
# category = whether you want counts by an age, weight, sex, or 'none' - just count all records
# value = the particular value you want to 
def query_counturl(drug_name, category, value):
    prefix = "https://api.fda.gov/drug/event.json?api_key=vZC1Gh1XyJl58wZKsMfJifZisDOFRsGBCij3G32v&search=patient.drug.openfda.brand_name:"
    q = "%22"
    suffix = "&count=patient.reaction.reactionmeddrapt.exact"
    return prefix + q + drug_name + q + suffix

#---------------------------------------------------------#
# GENERAL query method, you have to provide the suffix of the URL
# returns the JSON dictionary
def query(urlsuffix):
    url = general_prefix + urlsuffix
    j = urllib2.urlopen(url)
    d = json.load(j)
    return d
#---------------------------------------------------------#

general_prefix = "https://api.fda.gov/drug/event.json?api_key=vZC1Gh1XyJl58wZKsMfJifZisDOFRsGBCij3G32v"

# query user for the input (string for drug name)
drug_name = raw_input("Drug name?: ")

limit = 1
init = query_drug(drug_name, limit)
counts = query_count(drug_name)
#print counts['results']
num_effects = len(counts['results'])
print num_effects

# total # of records for that drug
total = init['meta']['results']['total'] 
# store a list of the effects (y)

# find the # of records associated with the age, weight, sex

sex = raw_input("Sex (Enter 1 for Male, 2 for Female): ")
age = raw_input("Age (Enter in Years): ")
weight = raw_input("Weight (Enter in kg): ")



# need to set the limit on the query = total # of records
# can only query 100 records at a time, so need to divide by 100 and query that many times
#data = query_drug(drug_name, total)
#print len(data['results'])

# process data
'''
analyze data here
Naive Bayes Algorithm
P(X|Y)= P(X and Y) + 1 / P(Y) - with Laplace smoothing
P(age|effect) = (P(age & effect) + 1) / P(effect) = # that are that age and had the effect / total # with that effect
NOTE: for ages, all the ages have specific units so need to convert them to years
i.e. query by each age TYPE and count the ones that fit the right #... need to convert from year > whatever the unit is and then query for that age
'''

# initialize the probability matrix
# rows = each effect (each y)
# each row = [P(Y), P(age|y), P(weight|y), P(gender|y)]
probs = numpy.ones((num_effects, 4))
effects = [] # store a list of effects in the same index order as the rows of probs

# 1. Find the counts of each of the adverse effects and how many adverse effects there are
total_count = 0 # to verify the 'count' variable above
for i in range(num_effects):
    #print counts['results'][i]['term']
    effects.append(counts['results'][i]['term'])
    probs[i, 0] = counts['results'][i]['count'] # set the P(Y) column equal to the count(y) - for now. Going to divide by the total later
    total_count += counts['results'][i]['count']

print total_count
#print total - total number of records will always be LESS than the total number of effects reported, because there can be >1 effect per record.

# 2. Calc probabilities

# For AGE and this particular drug - assume code of 
agecounts = query("&search=patient.drug.openfda.brand_name:%22" + drug_name + "%22+AND+patient.patientonsetageunit:%22801%22+AND+patient.patientonsetage:%22" + str(age) + "%22&count=patient.reaction.reactionmeddrapt.exact")
for result in agecounts['results']:
    if result['term'] in effects:
        idx = effects.index(result['term'])
        probs[idx, 1] += result['count']
    else: # get rid of this later
        print str(result['term']) + " " + str(result['count'])

print ("---------------------------------------------")
weightcounts = query("&search=patient.drug.openfda.brand_name:%22" + drug_name + "%22+AND+patient.patientweight:%22" + str(weight) + "%22&count=patient.reaction.reactionmeddrapt.exact")
for result in weightcounts['results']:
    if result['term'] in effects:
        idx = effects.index(result['term'])
        probs[idx, 2] += result['count']
    else: # get rid of this later
        print str(result['term']) + " " + str(result['count'])

print ("---------------------------------------------")
sexcounts = query("&search=patient.drug.openfda.brand_name:%22" + drug_name + "%22+AND+patient.patientsex:%22" + str(sex) + "%22&count=patient.reaction.reactionmeddrapt.exact")
for result in sexcounts['results']:
    if result['term'] in effects:
        idx = effects.index(result['term'])
        probs[idx, 3] += result['count']
    else: # get rid of this later
        print str(result['term']) + " " + str(result['count'])
   
overall_probs = []     
for i in range(num_effects):
    probs[i, 1] = numpy.log(probs[i,1] / float(probs[i,0]))
    probs[i, 2] = numpy.log(probs[i,2] / float(probs[i,0]))
    probs[i, 3] = numpy.log(probs[i,3] / float(probs[i,0]))
    probs[i, 0] = numpy.log(probs[i, 0] / float(total_count))
    overall_probs.append(probs[i].sum())

print ("---------------------------------------------")
zipped = sorted(zip(effects, overall_probs), key=operator.itemgetter(1), reverse=True)
print zipped