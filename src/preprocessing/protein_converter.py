import csv
from glob import glob
from lxml import etree
import re

FILES = glob('/scratch/ajr619/fml/clinical/*/*.xml') 
FILES.sort()

PATIENT_FILES = glob("/scratch/ajr619/fml/*/Level_3/*.sorted")
PATIENT_FILES.sort()

patients = dict()
id = 0
for file in PATIENT_FILES:

    m = re.search("TCGA-..-([A-Za-z0-9]{4,4})-(\d{2,2})[A-Za-z]", file)
    patient_id = m.group(1)

    if patient_id not in patients:
        id = id + 1
        patients[patient_id] = id;


for file in FILES:
    tree = etree.parse(file)
    root = tree.getroot()
    nsmap = root.nsmap
    bio_specimen = root.xpath('//bio:bcr_shipment_portion_uuid', namespaces=nsmap)
    if len(bio_specimen) == 0:
        continue

    filename = bio_specimen[0].text

    tissues_and_patients = root.xpath('//bio:bcr_sample_barcode', namespaces=nsmap)
    patient_text = None
    old_patient_names = None

    for t_p in tissues_and_patients:
        tp = t_p.text
        m = re.search("TCGA-..-([A-Za-z0-9]{4,4})-(\d{2,2})[A-Za-z]", tp)
        patient_text = m.group(1)
        tissue_type = m.group(2)

        if old_patient_names is not None and  old_patient_names != patient_text:
            print "Patient name doesn't match", file, patient_text, old_patient_names

        if patient_text not in patients:
            id = id + 1
            patients[patient_text] = id;

        old_patient_names = patient_text
        patient_id = patients[patient_text]
