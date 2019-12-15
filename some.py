from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
import datetime
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
import math

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd = '',  
    database='ind' 
)

mycursor = mydb.cursor()

    toi_idf= "SELECT * from toi"
    bbc_idf = "SELECT * from bbc"
    hind_idf = "SELECT * from hindtimes"

    mycursor.execute(toi_idf)
    l = mycursor.fetchall()
    mycursor.execute(bbc_idf)
    m = mycursor.fetchall()
    mycursor.execute(hind_idf)
    n = mycursor.fetchall()
    idf=[]
    h=[]
    o =[]
    q = []
    unique_words = []
    for i in range(len(l)):
        h.append([l[i][3]])
        

    for i in range(len(m)):
        o.append([l[i][3]])
        

    for i in range(len(n)):
        q.append([l[i][3]])
        
    for l in h:
        for j in range(len(l)):
            if l[j] not in unique_words:
                lis = str.split(l[j])
                for p in lis:
                    if p not in unique_words:
                        unique_words.append(p)
    for l in o:
        for j in range(len(l)):
            if l[j] not in unique_words:
                lis = str.split(l[j])
                for p in lis:
                    if p not in unique_words:
                        unique_words.append(p)
    for l in q:
        for j in range(len(l)):
            if l[j] not in unique_words:
                lis = str.split(l[j])
                for p in lis:
                    if p not in unique_words:
                        unique_words.append(p)


    for word in unique_words:
        count = 0    
        for i in range(len(h)):
            peek = str(h[i])
            lis = str.split(peek)
            if word in lis:
                count += 1
        
        for i in range(len(o)):
            peek = str(h[i])
            lis = str.split(peek)
            if word in lis:
                count += 1
        
        for i in range(len(q)):
            peek = str(h[i])
            lis = str.split(peek)
            if word in lis:
                count += 1
        
        idf.append([word,count])
            #if word in h[i]:

    sum_idf = 517
    for i in idf:
        if i[1]>0:
            i[1]=math.log(517/i[1])

    print(idf)


    


