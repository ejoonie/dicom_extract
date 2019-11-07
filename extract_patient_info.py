import pydicom as dicom
import os
import pandas as pd
import csv
from datetime import datetime

# config
# Specify the .dcm folder path
# folder_root_path = "/Volumes/GoogleDrive/My Drive/Asan Image Research/AIR_Research/04 Data/경희대 200건 유명원 PRE&POST/PRE"
dicom_root_path = "./dicom_sample"

# Current date and time
now = datetime.now()


def get_fieldnames():
    """
    여러곳에서 재 사용하기 위해 만든 함수
    뽑아야 할 다이콤 필드 리스트를 반환한다.
    :return: tag array
    """
    dicom_tags = pd.read_csv('./dicom_tags.csv')
    return list(dicom_tags['Description'])


def folder_to_csv(folder_name):
    """
    폴더 안에 있는 다이콤 파일들을 읽어서 csv 로 빼는 함수
    안쓸예정
    :param folder_name:
    :return: none
    """
    folder_path = os.path.join(dicom_root_path, folder_name)
    images_path = os.listdir(folder_path)
    # Patient's information will be stored in working directory #'Patient_Detail_Info.csv'
    with open(now.strftime("%y%m%d") + " " + folder_name + '.csv', 'w', newline='') as csvfile:
        fieldnames = get_fieldnames()
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fieldnames)
        for n, image in enumerate(images_path):
            ds = dicom.dcmread(os.path.join(folder_path, image), force=True)
            row = []
            for field in fieldnames:
                if field not in ds or ds.data_element(field) is None:
                    row.append('')
                else:
                    x = str(ds.data_element(field)).replace("'", "")
                    y = x.find(":")
                    x = x[y + 2:]
                    row.append(x)
            writer.writerow(row)


def folder_to_array(folder_name):
    """
    폴더 안에 있는 다이콤 파일들을 읽어서 array 로 빼는 함수
    :param folder_name:
    :return: array
    """
    folder_path = os.path.join(dicom_root_path, folder_name)
    images_path = os.listdir(folder_path)

    rows = []
    fieldnames = get_fieldnames()
    for n, image in enumerate(images_path):
        ds = dicom.dcmread(os.path.join(folder_path, image), force=True)
        row = []
        for field in fieldnames:
            if field not in ds or ds.data_element(field) is None:
                row.append('')
            else:
                x = str(ds.data_element(field)).replace("'", "")
                y = x.find(":")
                x = x[y + 2:]
                row.append(x)
        rows.append(row)

    return rows


#
# main
#
print("Root dir is %s" % dicom_root_path)
all_rows = []
# 1. 전체 다 까서 한 배열에 집어 넣은 다음에
for directory in os.listdir(dicom_root_path):
    if os.path.isdir(os.path.join(dicom_root_path, directory)):
        # folder_to_csv(directory) # 테스트용
        rows = folder_to_array(directory)
        all_rows += rows

# 2. csv 로 한꺼번에 출력 - 파일이름은 날짜_all.csv
outfile_name = now.strftime("%y%m%d") + "_all" + '.csv'
with open(outfile_name, 'w', newline='') as csvfile:
    # writer 생성
    writer = csv.writer(csvfile, delimiter=',')

    # 헤더 출력
    writer.writerow(get_fieldnames())

    # 데이터 출력
    for row in all_rows:
        writer.writerow(row)
