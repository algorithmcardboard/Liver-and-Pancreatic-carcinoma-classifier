import csv
from glob import glob

keys = list()
keys.extend(['PatientID', 'CancerType'])

with open('/scratch/ajr619/fml/protein/all_data/keys','r') as keyFile:
    keyF = csv.reader(keyFile)
    for row in keyF:
        keys.extend(row)

inCsv = csv.reader(open('/scratch/ajr619/fml/clinical/tmp.file.csv.actual'), delimiter=',')
outCsv = csv.DictWriter(open('/scratch/ajr619/fml/clinical/data.csv','w'), fieldnames=keys, restval=0.0,extrasaction='raise')

file_pattern = '/scratch/ajr619/fml/protein/all_data/mdanderson.org_{0}.MDA_RPPA_Core.protein_expression.Level_3.{1}.txt.sorted'

print "number of keys is ", len(keys)

cancer_pattern = {1:'PAAD', 2:'LIHC'}

for row in inCsv:
    filename = file_pattern.format(cancer_pattern[int(row[1])], row[0])
    with open(filename, 'r') as myFile:
        out = dict()
        out['PatientID'] = row[2]
        out['CancerType'] = row[1]

        r = csv.reader(myFile, delimiter='\t')
        for line in r:
            out[line[0]] = line[1]
        
        outCsv.writerow(out)

