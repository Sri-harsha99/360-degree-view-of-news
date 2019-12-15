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

source = requests.get('https://www.hindustantimes.com/india-news/').text

for i in range(2,25):
    link=str('https://www.hindustantimes.com/india-news/page/?pageno={}'.format(i))
    match.append(link)
    
soup = BeautifulSoup(source,features='lxml')
for link in soup.find_all('a', href=True):
    links.append(link['href'])
#'^/news.*\d{8}$'
for link in links:
    test = (re.search('^https://www.hindustantimes.com/india-news/.*/story-.*$', link))
    if test != None:
        match.append(link)

match = list(dict.fromkeys(match))

#print(match)


count = -1
count2=0
count3 = 0
while count<5000:
    count +=1
    news = requests.get(match[count]).text
    beu = BeautifulSoup(news,features='lxml')
    for newlink in beu.find_all('a', href=True):    
         
        test = (re.search('^https://www.hindustantimes.com/india-news/.*/story-.*$',newlink['href'])) 
       
        if test != None:
            l=test.group(0)
           # l = str("https://timesofindia.indiatimes.com")+str(l)
            if l not in match:
                match.append(l)
    date = ''
    dates=''
    finaldate=''
    namestext= ''
    art_text = ''
    try:
        article = beu.find('div',class_='storyArea')
        date= beu.find('span',class_='text-dt')
    except:
        article = None
        date=None

    if date!=None:
        dates=date.text
        dates = str(dates)
        dates = dates.strip()
        datelist = re.split(r':',dates)
        datelist = re.split(r',',datelist[1])
        datelist = str(datelist[0])+ str(' ')+str('2019')
        date_time_obj = datetime.datetime.strptime(datelist, ' %b %d %Y')
        print('Date:', date_time_obj.date())
        dat = str(date_time_obj.date())
        #-12 to -22
    article_text=''
    title=''
    sqlname=''
    sqldate=''
    if article != None:  
        print(match[count])  
        #
        #article_text =  beu.find('div',class_='storyDetail')
        #for x in article_text:
        #    print(x.find('p'))
        
        #art_text= str(art_text)+str(x.find('p').text)
        summary = beu.find('div',class_='storyDetail').findAll('p')
        for element in summary:
            article_text += '\n' + ''.join(element.findAll(text = True))

        #print(article_text)
        title = article.h1.text

    if title !='' and article_text !='':
        print('********************************')
        sql = "INSERT INTO hindtimes (title,body,names,date,url) VALUES (%s,%s,%s,%s,%s)"  
    
        names= extract_names(article_text) 
        for name in names:
            namestext = str(namestext) +str(" ") +str(name)  
        
        url = match[count]
        print(url)
 
        tup = (title,article_text,namestext,dat,url)
        
        try:
            mycursor.execute(sql,tup)    
            mydb.commit()
        except:
            print("error")
            
    
            
        
        