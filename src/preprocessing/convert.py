import csv
from glob import glob
import re

FILES = glob("/scratch/ajr619/fml/*/Level_3/*.sorted")
FILES.sort()

OUT_FILE = '/scratch/ajr619/fml/output_file'

output_writer = open(OUT_FILE, 'a')

patients = dict()
id = 0

for file in FILES:
    print "processing file ", file
    output_writer.write("\n")

    m = re.search("TCGA-..-([A-Za-z0-9]{4,4})-(\d{2,2})[A-Za-z]", file)
    patient_id = m.group(1)
    tissue_type = m.group(2)

    if patient_id not in patients:
        id = id + 1
        patients[patient_id] = id;

    patient_id = patients[patient_id]

    cancer_type = 2
    tmp = re.search("PAAD", file)
    if tmp is not None:
        cancer_type = 1

    output_writer.write("{0} {1} {2} ".format(patient_id, cancer_type, tissue_type))
    with open(file, 'r') as myFile:
        reader = csv.reader(myFile, delimiter='\t')
        for row in reader:
            try:
                beta_value = row[1]
                if beta_value == 'NA':
                    beta_value = '0.0'
                beta_value = float(beta_value)
                output_writer.write(str(beta_value))
            except ValueError as e:
                output_writer.write('0.0')
                print "Exception wile reading line ", reader.line_num, " from file ", file, "  Expeced a float. Got ", beta_value

            output_writer.write(" ")
