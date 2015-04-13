'''
Created on Apr 13, 2015

@author: gmccabe
'''
import single_drug_all
import sys
#import single_drug_all 
from distutils.tests.test_register import RawInputs
from sys import argv
import urllib2
# import module for working with JSON files
import json

def main():
    drug_name = raw_input('enter a drug name :')
# load query result in json format
    URL = single_drug_all.query(drug_name)
    j = urllib2.urlopen(URL)
    data = json.load(j)
    #sys.argv[1] = 'Lipitor'
    #drug_name = raw_input('enter a drug name :')
    #single_drug_all.query(drug_name)
    
if __name__ == '__main__':
    main()