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
    advisor = ''
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
            # pix.save("test.png")
            text = pytesseract.image_to_string(img)
            text = text.split('\n')
            text = [s for s in text if s]
            # print(text)
            try:
                students_index = text.index('With Student Advisor')
                advisor_index = text.index('With Student Advisor') + 1
            except:
                try:
                    students_index = text.index('With Faculty Advisor')
                    advisor_index = text.index('With Faculty Advisor') + 1
                except:
                    try:
                        students_index = text.index('Of') - 1
                        advisor_index = text.index('Of') - 1
                    except:
                        students_index = text.index('Was Designated As') - 3
                        advisor_index = text.index('Was Designated As') - 2
            # print(students_index)
            # print(advisor_index)
            try:
                univ_index = text.index('Was Designated As') - 1
                students = text[0:students_index]
                advisor = text[advisor_index]
                university = text[univ_index]
            except:
                students = text[0:3]
                advisor = text[4]
                university = text[5]
            prize = text[-1]

        pdf.close()
    except:
        print(control_number, 'Exception')
        with open('exception.txt', 'w+') as exception_file:
            exception_file.write(str(control_number))

    university = university.replace(',', ' ').replace('1', 'i')
    prize = prize.replace(',', ' ')
    advisor = advisor.replace(',', ' ').replace('1', 'i')
    stus = []
    for student in students:
        student = student.replace(',', ' ').replace('1', 'i')
        stus.append(student)
    return stus, advisor, university, prize


def savetext(start, end, count):
    global logger
    all_data = ''
    your_university_data = ''
    for control_number in range(start, end):
        control_number = '%05d' % control_number
        control_number = year * 100000 + int(control_number)
        path = "./paper_20" + str(year) + "/" + str(control_number) + ".pdf"
        # print(path)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            students, advisor, university, prize = pdf2text(path, control_number)
            if prize:
                if len(students) == 0:
                    students = ', , '
                elif len(students) == 1:
                    students = ','.join(students) + ', , '
                elif len(students) == 2:
                    students = ','.join(students) + ', '
                elif len(students) == 3:
                    students = ','.join(students)
                elif len(students) > 3:
                    students = students[0:3]
                    students = ','.join(students)

                row = '%s,%s,%s,%s,%s,\n' % (control_number, students, advisor, university, prize)
                row = row.encode('gbk', 'backslashreplace').decode('gbk', 'backslashreplace')
                try:
                    print(row)
                except:
                    print(control_number, ' -- gbk encoding error')

                all_data += row
                if university == your_university:
                    your_university_data += row

    with open('./all/tmp' + str(count) + '.txt', 'w', encoding='utf-8') as all_file:
        # all_data = all_data.encode('utf-8')
        all_file.write(all_data)
        print('./all/tmp' + str(count) + '.txt save sucessfully')
    with open('./your_university/tmp' + str(count) + '.txt', 'w', encoding='utf-8') as your_university_file:
        your_university_file.write(your_university_data)
        print('./your_university/tmp' + str(count) + '.txt save sucessfully')


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

    # students, advisor, university, prize = pdf2text('./paper_2023/2300009.pdf', 2300009)
