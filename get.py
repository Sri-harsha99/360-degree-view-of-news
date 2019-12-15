from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
import datetime
import datetime
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')



mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd = '',  
    database='ind' 
)

print(mydb)

mycursor = mydb.cursor()

def monthtonum(month):
    return{
        'January' : 1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9, 
        'October' : 10,
        'November' : 11,
        'December' : 12
}[month]

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

date_time_obj=datetime.datetime.now()


links=[]
test=''
match=[]
newlinks=[]
datelist=[]

source = requests.get('https://www.bbc.com/news/world/asia/india').text

soup = BeautifulSoup(source,features='lxml')
for link in soup.find_all('a', href=True):
    links.append(link['href'])
#'^/news.*\d{8}$'
for link in links:
    test = (re.search('^/news/world-asia-india.*\d{8}$', link))
    if test != None:
        match.append(link)

for i in range(len(match)):
    match[i] = str('https://www.bbc.com') + str(match[i])

match = list(dict.fromkeys(match))

print(match)


count = 0
for link in match:
    count +=1
    news = requests.get(link).text
    beu = BeautifulSoup(news,features='lxml')
    for newlink in beu.find_all('a', href=True):
        newlinks.append(newlink['href'])
    #'^/news.*\d{8}$'
    for newlink in newlinks:
        test = (re.search('^/news/world-asia-india.*\d{8}$', newlink))
        if test != None:
            l=str('https://www.bbc.com') + str(newlink)
            if l not in match:
                match.append(l)

    try:
        article = beu.find('div',class_='story-body')
        date= beu.find('div',class_='date date--v2').text
    except:
        article = None
        date = None
    if date !=None:
        paper = 'bbc'
        article_text=''
        namestext=''
        print(date)
        strdate = ''
        date = str(date)
        datelist = date.split(' ')
        print(datelist[1])
        month=monthtonum(datelist[1])
        datelist[1]=month
        strdate = str(datelist[0])+str(' ')+str(datelist[1])+str(' ')+str(datelist[2])
        print(strdate)
    if article != None:    
        summary = beu.find('div',class_='story-body__inner').findAll('p')
        for element in summary:
            article_text += '\n' + ''.join(element.findAll(text = True))
        title = article.h1.text
    if title !='' and article_text !='':
        sql = "INSERT INTO bbc (title,body,names,date) VALUES (%s,%s,%s,%s)"
        names= extract_names(article_text)
        for name in names:
            namestext = str(namestext) +str(" ") +str(name)  
        print(namestext)  
        tup = (title,article_text,namestext,strdate)
        try:
            mycursor.execute(sql,tup)   
            print(title)
            print(article_text) 
            mydb.commit()
        except:
            pass

        
 

