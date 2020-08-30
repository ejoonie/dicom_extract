# coding=utf-8
import pydicom as dicom
import os
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import PIL
import numpy as np
import shutil
# GUI로 dicom_root_path 선택
from tkinter import filedialog
from tkinter import *


# config
nowdate = datetime.now().strftime('%y%m%d')


# root 경로 입력
# dicom_root_path = '/Users/yousunko/Downloads/test'  # change

root_path = Tk()
dicom_root_path = filedialog.askdirectory()

# root_path.dirName = filedialog.askdirectory()
# dicom_root_path = root_path.dirName

output_img_dir = 'output_img'
output_img_subdir = output_img_dir + "/" + nowdate + "_" + os.path.basename(dicom_root_path)  # root 경로에 있는 디렉토리 이름으로 넣어줘야 함
output_csv_dir = 'output_csv'  # root 경로에 있는 디렉토리 이름으로 넣어줘야 함

# 폴더 없으면 새로 생성
if not os.path.exists(output_img_dir):
    print("Directory does not exist. Creating %s" % output_img_dir)
    os.mkdir(output_img_dir)

def get_fieldnames():
    """
    여러곳에서 재 사용하기 위해 만든 함수
    뽑아야 할 다이콤 필드 리스트를 반환한다.
    :return: tag array
    """
    dicom_tags = pd.read_csv('./dicom_CT_one.csv')  # change

    return list(dicom_tags['Description'])


# def folder_to_csv(folder_name):
#     """
#     폴더 안에 있는 다이콤 파일들을 읽어서 csv 로 빼는 함수
#     안쓸예정
#     :param folder_name:
#     :return: none
#     """
#     now = datetime.now()
#     folder_path = os.path.join(dicom_root_path, folder_name)
#     images_path = os.listdir(folder_path)
#     # Patient's information will be stored in working directory #'Patient_Detail_Info.csv'
#     with open(now.strftime("%y%m%d") + " " + folder_name + '.csv', 'w', newline='') as csvfile:
#         fieldnames = get_fieldnames()
#         writer = csv.writer(csvfile, delimiter=',')
#         writer.writerow(fieldnames)
#         for n, image in enumerate(images_path):
#             ds = dicom.dcmread(os.path.join(folder_path, image), force=True)
#             row = []
#             for field in fieldnames:
#                 if field not in ds or ds.data_element(field) is None:
#                     row.append('')
#                 else:
#                     x = str(ds.data_element(field)).replace("'", "")
#                     y = x.find(":")
#                     x = x[y + 2:]
#                     row.append(x)
#             writer.writerow(row)


def files_to_array(input_folder_name):
    """
    폴더 안에 있는 다이콤 파일들을 모두 읽어서 array 로 빼는 함수
    :param input_folder_name:
    :return: array
    """
    input_folder_path = os.path.join(dicom_root_path, input_folder_name)
    dicom_files_list = os.listdir(input_folder_path)

    rows_all = []
    fieldnames = get_fieldnames()
    for n, image in enumerate(dicom_files_list):
        ds = dicom.dcmread(os.path.join(input_folder_path, image), force=True)
        row = []
        row.append(input_folder_name)
        row.append(os.path.basename(image))
        for field in fieldnames:
            if field not in ds or ds.data_element(field) is None:
                row.append('')
            else:
                x = str(ds.data_element(field)).replace("'", "")
                y = x.find(":")
                x = x[y + 2:]
                row.append(x)
        rows_all.append(row)

    return rows_all


def file_to_array(input_folder_name):
    """
    폴더 안에 있는 다이콤 파일 중 하나를 (중간 위치) 읽어서 array 로 빼는 함수
    :param input_folder_name:
    :return: array
    """
    folder_path = os.path.join(dicom_root_path, input_folder_name)

    # dicom_files = os.listdir(folder_path)
    # dicom_files.sort()  # 이름순 정렬
    dicom_files_list = os.listdir(folder_path)
    # .dcm 파일만 선택
    dicom_files = [file for file in dicom_files_list if file.endswith(".dcm")]
    dicom_files.sort()  # 이름순 정렬
    select_img = dicom_files[int(len(dicom_files) / 2)]

    rows_all = []
    fieldnames = get_fieldnames()
    # for n, image in enumerate(images_path):
    ds = dicom.dcmread(os.path.join(folder_path, select_img), force=True)
    row = []
    row.append(input_folder_name)
    row.append(os.path.basename(select_img))
    for field in fieldnames:
        if field not in ds or ds.data_element(field) is None:
            row.append('')
        else:
            x = str(ds.data_element(field)).replace("'", "")
            y = x.find(":")
            x = x[y + 2:]
            row.append(x)
    rows_all.append(row)

    return rows_all


def folder_to_img(select_img, input_folder_name,
                  output_folder_name,
                  input_file_name=None,
                  output_file_name=None):
    """
    폴더 안에 있는 다이콤 파일들을 읽어서 중간 다이콤 파일을 이미지로 출력
    폴더 안 특정 파일을 뽑아내고 싶을땐 파일 이름을 지정해 주면 됨
    e.g)
    1. folder_to_img('dir01') => 폴더안 중간 파일
    2. folder_to_img('dir01', '0045.dcm') => 폴더안 0045.dcm 파일을 jpeg or png 으로
    :param input_folder_name: 다이콤파일들이 있는 디렉토리
    :param output_folder_name: 이미지 저장 장소
    :param input_file_name: None 이면 디폴트 파일을 읽고, 지정하면 지정 파일을 출력
    :param output_file_name: None 이면 있으면 이 파일을 읽고, 없으면 디폴트
    :return: array
    """
    input_folder_path = os.path.join(dicom_root_path, input_folder_name)
    output_folder_path = os.path.join('./', output_folder_name)

    dicom_files_list = os.listdir(input_folder_path)
    # .dcm 파일만 선택
    dicom_files = [file for file in dicom_files_list if file.endswith(".dcm")]
    dicom_files.sort()  # 이름순 정렬

    # 폴더 없으면 새로 생성
    if not os.path.exists(output_folder_path):
        print("Directory does not exist. Creating %s" % output_folder_name)
        os.mkdir(output_folder_path)

    # input_file_name 을 정했으면 그대로사용, 아니면 중간파일
    # 파일의 시작은 0, 마지막 파일은 int(len(dicom_files) - 1
    tmp = {'0': 0,
           '1': len(dicom_files) - 1,
           '2': int(len(dicom_files) / 2)}
    input_file_name = input_file_name or dicom_files[tmp[select_img]]

    # output_file_name 의 디폴트를 "1801-01_00001.png" 같이 나오게 설정
    default_img_file_name = "%s_%s.png" % (input_folder_name, input_file_name.replace(".dcm", ""))

    # output_file_name 을 정했으면 그대로 사용, 아니면 디폴트
    output_file_name = output_file_name or default_img_file_name

    # path 설정
    input_file_path = os.path.join(input_folder_path, input_file_name)
    output_file_path = os.path.join(output_folder_path, output_file_name)

    # 어떤거 변환하는지 출력
    print("%s => %s" % (input_file_path, output_file_name))

    # 실제 변환
    try:
        dicom_to_img(input_file_path, output_file_path)
    except:
        print("이미지변환 에러발생: %s" % output_file_name)


def transform_to_hu(ds, pixel_array):
    intercept = ds.RescaleIntercept
    slope = ds.RescaleSlope
    hu_image = pixel_array * slope + intercept

    return hu_image


def window_image(pixel_array, window_center, window_width):
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    window_image = pixel_array.copy()
    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max

    return window_image


def dicom_to_img(input_file_path, output_file_path):
    ds = dicom.dcmread(input_file_path, force=True)
    pixel_array = ds.pixel_array
    # shape = pixel_array.shape
    # image_2d = pixel_array.astype(float)
    # image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
    # image_2d_scaled_uint8 = np.uint8(image_2d_scaled)

    hu_image = transform_to_hu(ds, pixel_array)
    L3_image = window_image(hu_image, 0, 400)

    plt.figure(figsize=(20, 10))
    plt.style.use('grayscale')

    # cv2.imwrite(output_file_path, image_2d_scaled_uint8)
    mpimg.imsave(output_file_path, L3_image)


def move_csv(output_csv_dir):
    # 폴더 없으면 새로 생성
    if not os.path.exists(output_csv_dir):
        print("Directory does not exist. Creating %s" % output_csv_dir)
        os.mkdir(output_csv_dir)

    # 당일 여러번 분석 시, 기존 생성한 csv 파일 삭제하고 다시 생성
    if os.path.isfile(os.path.join('./', output_csv_dir, outfile_name)):
        os.remove(os.path.join('./', output_csv_dir, outfile_name))
        shutil.move(os.path.join('./', outfile_name), output_csv_dir)
    else:
        shutil.move(os.path.join('./', outfile_name), output_csv_dir)


#
# main
#
print("Root dir is %s" % dicom_root_path)

all_or_one = input('Extract information to all DCM files? (y or n): ')
total_rows = []

get_img = input('Extract PNG files from DCM files? (y or n): ')

if all_or_one == 'y':
    # image 출력 시 어떤 이미지 선택?
    if get_img == 'y':
        select_img = input('Enter one of the following numbers (First [0] or End [1] or Middle [2]): ')

        # 1. 전체 다 까서 한 배열에 집어 넣은 다음에
        for input_folder_name in os.listdir(dicom_root_path):  # [0:x] 0 부터 .. x 까지
            if os.path.isdir(os.path.join(dicom_root_path, input_folder_name)) and input_folder_name != output_img_subdir:
                # 디렉토리 이름을 출력해줘야 진행상황 알 수 있음
                print("%s" % input_folder_name)

                # 폴더별 이미지 출력
                folder_to_img(select_img, input_folder_name, output_img_subdir)

                # 데이터 추출 및 합치기
                rows = files_to_array(input_folder_name)
                total_rows += rows

        # 2. 합친 데이터를 csv 로 한꺼번에 출력 - 파일이름은 날짜_상위폴더명_all.csv
        outfile_name = nowdate + "_" + os.path.basename(dicom_root_path) + "_all" + '.csv'
        with open(outfile_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # writer 생성
            writer = csv.writer(csvfile, delimiter=',')

            # 헤더 출력
            writer.writerow(['directory_name'] + ['file_name'] + get_fieldnames())

            # 데이터 출력
            for row in total_rows:
                writer.writerow(row)
    else:
        # 1. 전체 다 까서 한 배열에 집어 넣은 다음에
        for input_folder_name in os.listdir(dicom_root_path):  # [0:x] 0 부터 .. x 까지
            if os.path.isdir(os.path.join(dicom_root_path, input_folder_name)) and input_folder_name != output_img_subdir:
                # 디렉토리 이름을 출력해줘야 진행상황 알 수 있음
                print("%s" % input_folder_name)

                # 데이터 추출 및 합치기
                rows = files_to_array(input_folder_name)
                total_rows += rows

        # 2. 합친 데이터를 csv 로 한꺼번에 출력 - 파일이름은 날짜_상위폴더명_all.csv
        outfile_name = nowdate + "_" + os.path.basename(dicom_root_path) + "_all" + '.csv'
        with open(outfile_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # writer 생성
            writer = csv.writer(csvfile, delimiter=',')

            # 헤더 출력
            writer.writerow(['directory_name'] + ['file_name'] + get_fieldnames())

            # 데이터 출력
            for row in total_rows:
                writer.writerow(row)

else:
    # image 출력 시 어떤 이미지 선택?
    if get_img == 'y':
        select_img = input('Enter one of the following numbers (First [0] or End [1] or Middle [2]): ')

        # 1. 전체 다 까서 한 배열에 집어 넣은 다음에
        for input_folder_name in os.listdir(dicom_root_path):  # [0:x] 0 부터 .. x 까지
            if os.path.isdir(os.path.join(dicom_root_path, input_folder_name)) and input_folder_name != output_img_subdir:
                # 디렉토리 이름을 출력해줘야 진행상황 알 수 있음
                print("%s" % input_folder_name)

                # 폴더별 이미지 출력
                folder_to_img(select_img, input_folder_name, output_img_subdir)

                # 데이터 추출 및 합치기
                rows = file_to_array(input_folder_name)
                total_rows += rows

        # 2. 합친 데이터를 csv 로 한꺼번에 출력 - 파일이름은 날짜_상위폴더명_all.csv
        outfile_name = nowdate + "_" + os.path.basename(dicom_root_path) + "_one" + '.csv'
        with open(outfile_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # writer 생성
            writer = csv.writer(csvfile, delimiter=',')

            # 헤더 출력
            writer.writerow(['directory_name'] + ['file_name'] + get_fieldnames())

            # 데이터 출력
            for row in total_rows:
                writer.writerow(row)

    else:
        # 1. 전체 다 까서 한 배열에 집어 넣은 다음에
        for input_folder_name in os.listdir(dicom_root_path):  # [0:x] 0 부터 .. x 까지
            if os.path.isdir(os.path.join(dicom_root_path, input_folder_name)) and input_folder_name != output_img_subdir:
                # 디렉토리 이름을 출력해줘야 진행상황 알 수 있음
                print("%s" % input_folder_name)

                # 데이터 추출 및 합치기
                rows = file_to_array(input_folder_name)
                total_rows += rows

        # 2. 합친 데이터를 csv 로 한꺼번에 출력 - 파일이름은 날짜_상위폴더명_all.csv
        outfile_name = nowdate + "_" + os.path.basename(dicom_root_path) + "_one" + '.csv'
        with open(outfile_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # writer 생성
            writer = csv.writer(csvfile, delimiter=',')

            # 헤더 출력
            writer.writerow(['directory_name'] + ['file_name'] + get_fieldnames())

            # 데이터 출력
            for row in total_rows:
                writer.writerow(row)

# 4. csv 파일 경로 이동
move_csv(output_csv_dir)

# 5. 하나만 출력할 경우 실행
# folder_to_img("Thigh01-0867_DCM_POST", output_img_subdir)
