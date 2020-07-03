# https://github.com/icometrix/dicom2nifti
# INSTALL: conda install -c conda-forge dicom2nifti OR pip install dicom2nifti
# UPDATE: conda update dicom2nifti OR pip install dicom2nifti --upgrade
# USAGE: dicom2nifti [-h] [-G] [-r] [-o RESAMPLE_ORDER] [-p RESAMPLE_PADDING] [-M] [-C] [-R] input_directory output_directory

import os
import dicom2nifti
from datetime import datetime
import shutil

# GUI로 dicom_root_path 선택
from tkinter import filedialog
from tkinter import *

root_path = Tk()
root_path.dirName = filedialog.askdirectory()
original_dicon_directory = root_path.dirName

# root 경로 입력
# original_dicon_directory = '/Users/Yousun/Desktop/test'  # change

# config
nowdate = datetime.now().strftime('%y%m%d')

output_folder_name = 'input'
output_file_dir = output_folder_name + '/' + os.path.basename(original_dicon_directory) # root 경로에 있는 디렉토리 이름으로 넣어줘야 함
# 폴더 없으면 새로 생성
if not os.path.exists(output_file_dir):
    print("Directory does not exist. Creating %s" % os.path.basename(original_dicon_directory))
    os.mkdir(output_file_dir)

output_file = 'img'

def move_nii(output_file_dir):
    # 당일 여러번 분석 시, 기존 생성한 csv 파일 삭제하고 다시 생성
    if os.path.isfile(os.path.join('./', output_file_dir, output_file + '.nii')):
        os.remove(os.path.join('./', output_file_dir, output_file + '.nii'))
        shutil.move(os.path.join('./', output_file + '.nii'), output_file_dir)
    else:
        shutil.move(os.path.join('./', output_file + '.nii'), output_file_dir)


# Converting a directory with dicom files to nifti files
# dicom2nifti.convert_directory(dicom_input, output_folder, compression=True, reorient=True)

# Converting a directory with only 1 series to 1 nifti file
dicom2nifti.dicom_series_to_nifti(original_dicon_directory, output_file, reorient_nifti=True)

move_nii(output_file_dir)