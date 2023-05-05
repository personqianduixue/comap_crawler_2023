"""
美赛获奖证书信息OCR
"""

import fitz
import PIL
import pytesseract
import os
from multiprocessing import Process
import re
from config import *

pytesseract.pytesseract.tesseract_cmd = TesseractOCR_path


def pdf2text(pdfPath, control_number, zoom_x=6, zoom_y=6, rotation_angle=0):
    students = ['']
    university = ''
    prize = ''
    try:
        # 打开PDF文件
        pdf = fitz.open(pdfPath)
        # 逐页读取PDF
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            rect = page.rect
            clip = fitz.Rect(rect.width * 0.25, rect.height * 0.27,
                             rect.width * 0.8, rect.height * 0.7)
            trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
            pix = page.get_pixmap(matrix=trans, alpha=False, clip=clip)
            img = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
            text = text.split('\n')
            text = [s for s in text if s]
            try:
                advisor_index = text.index('With Student Advisor')
            except:
                try:
                    advisor_index = text.index('With Faculty Advisor')
                except:
                    advisor_index = text.index('Was Designated As') - 3
            try:
                univ_index = text.index('Was Designated As') - 1
                students = text[0:advisor_index]
                university = text[univ_index]
            except:
                students = text[0:3]
                university = text[5]
            prize = text[-1]
            # pix.save(imgPath + str(pg) + ".png")
        pdf.close()
    except:
        print(control_number, 'Exception')
        with open('exception.txt', 'w+') as exception_file:
            exception_file.write(control_number)

    return students, university, prize


def savetext(start, end, count):
    global logger
    all_data = ''
    your_university_data = ''
    for control_number in range(start, end):
        control_number = '%05d' % control_number
        control_number = year * 100000 + int(control_number)
        path = "./paper/" + str(control_number) + ".pdf"
        if os.path.exists(path):
            students, university, prize = pdf2text(path, control_number)
            if len(students) == 1:
                students = ','.join(students) + ', , '
            elif len(students) == 2:
                students = ','.join(students) + ', '
            else:
                students = ','.join(students)

            row = '%s,%s,%s,\n' % (students, university, prize)
            if prize:
                num_row = '%s,%s' % (control_number, row)
                num_row = num_row.encode('gbk', 'backslashreplace').decode('gbk', 'backslashreplace')
                try:
                    print(num_row)
                except:
                    print(control_number, ' -- gbk encoding error')

                all_data += num_row
                if university == your_university:
                    your_university_data += num_row

    with open('./all/all' + str(count) + '.txt', 'w', encoding='utf-8') as all_file:
        # all_data = all_data.encode('utf-8')
        all_file.write(all_data)
        print('./all/all' + str(count) + '.txt save sucessfully')
    with open('./your_university/your_university' + str(count) + '.txt', 'w', encoding='utf-8') as your_university_file:
        your_university_file.write(your_university_data)
        print('./your_university/your_university' + str(count) + '.txt save sucessfully')


def txtjoint(dir):
    files = os.listdir(dir)
    res = 'control_number,student1,student2,student3,university,prize,'
    for file in files:
        with open(dir + file, "r", encoding='utf-8') as f:
            content = f.read()
            res += content

    with open(dir + "all.txt", "w", encoding='utf-8') as outFile:
        outFile.write(res)
        outFile.close()


if __name__ == '__main__':

    if not os.path.exists('./all/'):
        os.mkdir('./all/')
    if not os.path.exists('./your_university/'):
        os.mkdir('./your_university/')

    step = pdf2text_step
    count = 1
    for i in range(1, total_num, step):
        start = i
        end = i + step - 1
        p = Process(target=savetext, args=(start, end, count))
        p.start()
        count += 1

    # 合并文件
    all_dir = "./all/"
    your_university_dir = './your_university/'
    txtjoint(all_dir)
    txtjoint(your_university_dir)
