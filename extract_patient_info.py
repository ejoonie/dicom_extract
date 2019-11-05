import pydicom as dicom
import os
import pandas as pd
import csv
from datetime import datetime

# Current date and time
now = datetime.now()

# list of attributes available in dicom image
dicom_image_description = pd.read_csv('dicom_image_description_patient_info.csv')

# Specify the .dcm folder path
folder_root_path = "/Volumes/GoogleDrive/My Drive/Asan Image Research/AIR_Research/04 Data/경희대 200건 유명원 PRE&POST/PRE"
# folder_root_path = "./dicom_sample"

def folder(folder_name):
    folder_path = os.path.join(folder_root_path, folder_name)
    images_path = os.listdir(folder_path)
    # Patient's information will be stored in working directory #'Patient_Detail_Info.csv'
    with open(now.strftime("%y%m%d") + " " + folder_name + '.csv', 'w', newline ='') as csvfile:
        fieldnames = list(dicom_image_description["Description"])
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fieldnames)
        for n, image in enumerate(images_path):
            ds = dicom.dcmread(os.path.join(folder_path, image), force=True)
            rows = []
            for field in fieldnames:
                if field not in ds or ds.data_element(field) is None:
                    rows.append('')
                else:
                    x = str(ds.data_element(field)).replace("'", "")
                    y = x.find(":")
                    x = x[y+2:]
                    rows.append(x)
            writer.writerow(rows)

# folder_name = output csv file name
for directory in os.listdir(folder_root_path):
    if os.path.isdir(os.path.join(folder_root_path, directory)):
        # print(directory)
        folder(directory)
