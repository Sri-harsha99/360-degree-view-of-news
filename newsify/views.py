from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector
import nltk
import math
import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
stop = stopwords.words('english')
tok = RegexpTokenizer(r'\w+')

def home(request):
    mydb = mysql.connector.connect(
        host='localhost',
        port='3306',
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

    
    # t_title = "SELECT title FROM toi"
    # mycursor.execute(t_title)
    # a = mycursor.fetchall()

    # b_title = "SELECT title FROM bbc"
    # mycursor.execute(b_title)
    # b = mycursor.fetchall()
    
    # jac = {}
    # for i in range(1,len(a)+1):
    #     jac[i] = 0
    #     toi = tok.tokenize(a[i-1][0])
    #     for j in range(1, len(b)+1):
    #         inter = 0
    #         union = 0
    #         bbc = tok.tokenize(b[j-1][0])
    #         for word in toi:
    #             if word in bbc:
    #                 inter += 1
    #         union = len(a) + len(b) - inter
    #         j = inter/union
    #         if jac[i] < j:
    #             jac[i] = j
    # print(jac)

    t_names = "SELECT * FROM toi"
    mycursor.execute(t_names)
    c = mycursor.fetchall()

    b_names = "SELECT * FROM bbc"
    mycursor.execute(b_names)
    d = mycursor.fetchall()

    h_names = "SELECT * FROM hindtimes"
    mycursor.execute(h_names)
    e = mycursor.fetchall()  

    cosine = {}
    res = []
    for i in range(1, len(c)+1):
        cosine[i] = 0
        t = tok.tokenize(c[i-1][3])
        t_data = tok.tokenize(c[i-1][2])
        y = 0
        for j in range(1, len(d)+1):
            b = tok.tokenize(d[j-1][3])
            b_data = tok.tokenize(d[j-1][2])

            un = []
            for word in t:
                if word not in un:
                    un.append(word)
            for word in b:
                if word not in un:
                    un.append(word)

            temp1 = [0] * len(un)
            temp2 = [0] * len(un)

            for k in range(len(un)):
                count = 0
                count1 = 0
                for w in t_data:
                    if w == un[k]:
                        count += 1
                if count != 0:
                    temp1[k] = 1 + math.log(count, 10)
                for w in b_data:
                    if w == un[k]:
                        count1 += 1
                if count1 != 0:
                    temp2[k] = 1 + math.log(count1, 10)
            z = np.dot(temp1, temp2)
            if cosine[i] < z:
                cosine[i] = z
                y = j
        if cosine[i] > 10:
            res.append([i, y, 0])
        else:
            res.append([i,None,0])


    for i in range(1, len(c)+1):
        cosine[i] = 0
        t = tok.tokenize(c[i-1][3])
        t_data = tok.tokenize(c[i-1][2])
        y = 0
        for j in range(1, len(e)+1):
            h = tok.tokenize(e[j-1][3])
            h_data = tok.tokenize(e[j-1][2])

            un = []
            for word in t:
                if word not in un:
                    un.append(word)
            for word in h:
                if word not in un:
                    un.append(word)

            temp1 = [0] * len(un)
            temp2 = [0] * len(un)

            for k in range(len(un)):
                count = 0
                count1 = 0
                for w in t_data:
                    if w == un[k]:
                        count += 1
                if count != 0:
                    # for g in range(len(idf)):
                    #     if idf[g][0] == un[k]:
                    #         temp1[k] = (1 + math.log(count, 10)) * idf[g][1]
                    #     else:
                    temp1[k] = 1 + math.log(count, 10)
                for w in h_data:
                    if w == un[k]:
                        count1 += 1
                if count1 != 0:
                    # for g in range(len(idf)):
                    #     if idf[g][0] == un[k]:
                    #         temp2[k] = (1 + math.log(count1, 10)) * idf[g][1]
                    #     else:
                    temp2[k] = 1 + math.log(count1, 10)
            z = np.dot(temp1, temp2)
            if cosine[i] < z:
                cosine[i] = z
                y = j
        if cosine[i] > 10:
            res[i-1][2] = y
        else:
            res[i-1][2] = None

    result = []
    for i in range(len(res)):
        if (res[i][0] != None) and (res[i][1] != None) and (res[i][2] != None):
            p = (res[i][0],)
            q = (res[i][1],)
            r = (res[i][2],)
            toi_com = "SELECT * FROM toi WHERE id = %s"
            bbc_com = "SELECT * FROM bbc WHERE id = %s"
            hindtimes_com = "SELECT * FROM hindtimes WHERE id = %s"
            mycursor.execute(toi_com, p)
            toi_a = mycursor.fetchall()
            mycursor.execute(bbc_com, q)
            bbc_a = mycursor.fetchall()
            mycursor.execute(hindtimes_com, r)
            hindtimes_a = mycursor.fetchall()
            result.append([toi_a, bbc_a, hindtimes_a])
    print(result[0])
    context = {'result':result}
    return render(request, '2.html',context)

def home1(request):
    return render(request, '2.html')