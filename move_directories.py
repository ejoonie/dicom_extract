import os
import shutil

# root_path = '../from_1691'
root_path = '/Users/Yousun/Downloads/test'

# 실수할 수도 있으므로 dry_run 을 설정해서 로그만 찍을 것인지
# 실제 작동도 진행할 것인지 결정한다.
# dry_run = True
dry_run = False

def move_directory(input_directory_path, output_directory_path):
    print("moving %s to %s" % (input_directory_path, output_directory_path))
    if not dry_run:
        shutil.move(input_directory_path, output_directory_path)


#
# main
#
print("Root dir is %s" % root_path)

for level1 in os.listdir(root_path): # level1 == test1
    level1_path = os.path.join(root_path, level1)
    if os.path.isdir(level1_path):
        # 디렉토리 이름을 출력해줘야 진행상황 알 수 있음
        print("> %s" % level1)

        for level2 in os.listdir(level1_path): # level2 == test1-1
            level2_path = os.path.join(level1_path, level2)
            if os.path.isdir(level2_path):
                # level2 이름 출력
                print(">> %s" % level2)

                move_directory(level2_path, root_path)

        # 2. deleting dir
        print("Deleting %s" % level1_path)
        if not dry_run:
            shutil.rmtree(level1_path)
