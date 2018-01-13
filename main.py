#coding=utf-8

import os
import csv
#read csv
csvfile = file('movie2011.csv','r')
reader = csv.reader(csvfile)
movie_nm = []

for line in reader:
    if line[0] != '' && line[0]!='Film' && line[0]!= 'Average':
        movie_nm.append(line[0])    
csvfile.close()

#读取电影数据
try:
    for x in movie_nm:
        #数据整理
        write_name = x.replace('_','+')#换掉空格，否则搜索时会丢失后面的内容
        write_name = write_name.replace('\'','')
        write_name = write_name.replace(':', '%3A')#片名中的冒号在url中是以%3A表示的
        if write_name.find('(')!= -1:
            write_name = write_name[:write_name.find('(')]#去掉括号内容，否则影响搜索结果
        #print "name is :" + write_name

        #把电影名写到中间文件中去，让爬虫读取。和原文机制是一样的，写一个，爬一个
        movie_name_file = open('movie_name.txt','w')
        try:
            movie_name_file.write(write_name)
        finally:
            movie_name_file.close()

        #该爬虫程序会从movie_name中读取电影名来爬虫
        os.system(r"scrapy crawl imdb")

finally:
