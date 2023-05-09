# comap_crawler
2023美赛爬虫

update:新增advisor列

美国大学生数学建模竞赛证书爬取及信息OCR识别分析

1. config.py中设置年份、线程数、你的学校、TesseractOCR路径等

2. download.py下载证书，由于有些证书只运行一次部分下载会失败，需要运行多次，确保全部下载

3. pdf2text.py识别学校、姓名、获奖等级、队伍ID等
4. txt_joint.py合并OCR识别的txt结果
5. analysis.ipynb分析数据

2023美赛结果，证书数量20858张，最终识别20818条信息

https://raw.githubusercontent.com/personqianduixue/comap_crawler_2023/master/all/all_2023.txt

cdn加速镜像：https://ghproxy.net/https://raw.githubusercontent.com/personqianduixue/comap_crawler_2023/master/all/all_2023.txt

![统计结果](https://cdn.jsdelivr.net/gh/personqianduixue/picbed/img202305091055579.png)

![image-20230509105732629](https://cdn.jsdelivr.net/gh/personqianduixue/picbed/img202305091057649.png)

2022美赛结果，证书数量27205张，最终识别27161条信息

https://raw.githubusercontent.com/personqianduixue/comap_crawler_2023/master/all/all_2022.txt

cdn加速镜像：https://ghproxy.net/https://raw.githubusercontent.com/personqianduixue/comap_crawler_2023/master/all/all_2022.txt

![统计结果](https://cdn.jsdelivr.net/gh/personqianduixue/picbed/img202305091056671.png)

![image-20230509105700188](https://cdn.jsdelivr.net/gh/personqianduixue/picbed/img202305091057210.png)
