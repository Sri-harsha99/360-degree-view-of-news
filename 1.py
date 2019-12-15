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
        port='3306',
        user='root',
        passwd = '',
        database='ind'
    )
mycursor = mydb.cursor()
com = "SELECT * FROM data"
mycursor.execute(com)
a = mycursor.fetchall()
print(a[0][4])