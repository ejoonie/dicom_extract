import os
import shutil

# dicom_root_path = '../from_1691'
dicom_root_path = '/Users/Yousun/Downloads/Dynamic(익명화)'

# 실수할 수도 있으므로 dry_run 을 설정해서 로그만 찍을 것인지
# 실제 작동도 진행할 것인지 결정한다.
# dry_run = True
dry_run = False

def move_file(input_file_path, output_file_path):
    print("moving %s to %s" % (input_file_path, output_file_path))
    if not dry_run:
        shutil.move(input_file_path, output_file_path)



#
# main
#
print("Root dir is %s" % dicom_root_path)

for each_folder in os.listdir(dicom_root_path):
    each_folder_path = os.path.join(dicom_root_path, each_folder)
    if os.path.isdir(each_folder_path):
        # 디렉토리 이름을 출력해줘야 진행상황 알 수 있음
        print("> %s" % each_folder)

        for subfolder in os.listdir(each_folder_path):
            subfolder_path = os.path.join(each_folder_path, subfolder)
            if os.path.isdir(subfolder_path):
                # sub folder 이름 출력
                print(">> %s" % subfolder)

                # 1. move files
                for file in os.listdir(subfolder_path):
                    # 파일이름 출력
                    file_path = os.path.join(subfolder_path, file)
                    target_path = os.path.join(each_folder_path, file)
                    print(">>> file: %s" % file)
                    move_file(file_path, target_path)

                # 2. deleting dir
                print("Deleting %s" % subfolder_path)
                if not dry_run:
                    os.rmdir(subfolder_path)
