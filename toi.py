from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
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

source = requests.get('https://timesofindia.indiatimes.com/india').text
match.append('https://timesofindia.indiatimes.com/india')
match.append('https://timesofindia.indiatimes.com')

for i in range(2,10):
    link=str('https://timesofindia.indiatimes.com/india/{}'.format(i))
    match.append(link)
    
soup = BeautifulSoup(source,features='lxml')
for link in soup.find_all('a', href=True):
    links.append(link['href'])
#'^/news.*\d{8}$'
for link in links:
    
    test = (re.search('^https://timesofindia.indiatimes.com/india/.*\d{8}.cms$', link))
    if test != None:
        match.append(link)

match = list(dict.fromkeys(match))



count = -1
count2=0
count3 = 0
while count<5000:
    count +=1
    print(len(match))
    news = requests.get(match[count]).text
    beu = BeautifulSoup(news,features='html.parser')
    for newlink in beu.find_all('a', href=True):        
        test = (re.search('^/india/.*\d{8}.cms$',newlink['href'])) 
        if test != None:
            l=test.group(0)
            l = str("https://timesofindia.indiatimes.com")+str(l)
            if l not in match:
                match.append(l)
    date = ''
    dates=''
    finaldate=''
    namestext= ''
    art_text = ''
    try:
        article = beu.find('div',class_='_1IaAp clearfix')
        date= beu.find('div',class_='_3Mkg- byline')
    except:
        article = None
        date=None
    if date!=None:
        dates=date.text
            
        dates = str(dates)
        dates = dates.strip()
        datelist = re.split(r':',dates)
        datelist = re.split(r',',datelist[1])
        datelist = str(datelist[0])+ str(datelist[1])
        date_time_obj = datetime.datetime.strptime(datelist, ' %b %d %Y')
        print('Date:', date_time_obj.date())
        dat = str(date_time_obj.date())
        #-12 to -22
    article_text=''
    title=''
    sqlname=''
    sqldate=''
    if article != None:    
        article_text =  beu.find('div',class_='_3WlLe clearfix').text
        title = article.h1.text
    
        print(article_text)
    if title !='' and article_text !='':
        paper = 'toi'
        sql = "INSERT INTO toi (Title,Body,date,names) VALUES (%s,%s,%s,%s)"  
        names= extract_names(article_text) 
        for name in names:
            namestext = str(namestext) +str(" ") +str(name)  
        print(namestext)   
 
        tup = (title,article_text,dat,namestext)
        try:
            mycursor.execute(sql,tup)    
        except:
            pass
        mydb.commit()
        print(title)
        print(article_text) 