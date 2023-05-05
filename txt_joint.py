import os
import re

def txtjoint(dir):
    files = os.listdir(dir)
    res = 'control_number,student1,student2,student3,university,prize,,,\n'

    for file in files:
        if re.search('^tmp(\d+).txt',file):
            with open(dir + file, "r", encoding='utf-8') as f:
                content = f.read()
            res += content

    with open(dir + "all.txt", "w", encoding='utf-8') as outFile:
        outFile.write(res)
        print('txtjoint sucessfully')

# 合并文件
all_dir = "./all/"
your_university_dir = './your_university/'
txtjoint(all_dir)
txtjoint(your_university_dir)