# comap_crawler
2023美赛爬虫

美国大学生数学建模竞赛证书爬取及信息OCR识别分析

1. config.py中设置线程数，你的学校，TesseractOCR路径等

2. download.py下载证书，由于有些证书只运行一次部分下载会失败，需要运行多次，确保全部下载

3. pdf2text.py识别学校、姓名、获奖等级、队伍ID等
4. analysis.ipynb分析数据

以下是2022美赛爬取，2023美赛出成绩后会第一时间爬取

https://github.com/personqianduixue/comap_crawler

download.py：多线程下载证书，大概用时1小时

pdf2text.py:  多线程pdf OCR信息提取，大概用时1.5小时

证书数量：27205

最终识别得到的信息条数：27161

https://raw.githubusercontent.com/personqianduixue/comap_crawler/master/all/all.txt

部分信息会识别错误，例如 i 识别成了 1 
