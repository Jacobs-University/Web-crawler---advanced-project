'''importing packages'''
import sqlite3
import frequent
import datetime
import re
import requests
from bs4 import BeautifulSoup

def sql_connection():
    '''Establising SQL connection'''
    sqlite_file = 'E:\DE\Sem3\AdvancedProject2\mytest4_db.sqlite'    # name of the sqlite database file
    try:
        conn=sqlite3.connect(sqlite_file)
        print ("Database connection established")
        return conn
    except Error:
        print (Error)

def sql_table(con):
    '''Defining SQL tables'''
    c=con.cursor()
    c.execute('CREATE TABLE if not exists keywords_list (id integer PRIMARY KEY AUTOINCREMENT, keyword varchar)')
    c.execute('CREATE TABLE if not exists features (id integer PRIMARY KEY AUTOINCREMENT, keyword string, date string, frequency integer, resource string)')
    c.execute('CREATE TABLE if not exists resources (id integer PRIMARY KEY AUTOINCREMENT, name text, webaddress varchar)')
    print ("tables created")
    con.commit()

def insert_table(con,keyword_data,resources_data):
    '''Adding keywords and webaddress to tables'''
    c=con.cursor()
    print (keyword_data)
    c.executemany('INSERT OR REPLACE INTO keywords_list (id,keyword) VALUES (?,?)',keyword_data)
    c.executemany('INSERT OR REPLACE INTO resources (id,name,webaddress) VALUES (?,?,?)',resources_data)
    print ("inserts successful")
    con.commit()

found_words=[]

def insert_data(record,con):
    '''Insert data into features table: index,keyword,date,frequency,source'''
    print ("in insert data method, type of record",type(record))
    print ("records is",record)
    flag=0
    c=con.cursor()
    #print (record)
#        print (type(index),type(keywrd),type(timestamp),type(freq))
    for each_ele in record:
        print (type(each_ele))
    if(flag==0):
        c.execute('INSERT INTO features (keyword,date,frequency,resource) VALUES (?,?,?,?)',record)
        flag=1
        con.commit()
        print ("inserting record successful")
    else:
        print ("inserting record unsuccessful")
    
def scraping(con,resources_data,keyword_data,index):
    for pos in range(0,len(keyword_data)):
        word=keyword_data[pos][1]
        #print ("keyword",word)
        for res_pos in range(0,len(resources_data)): 
            source=resources_data[res_pos][2]
            found_words.append(word)
            result=frequent.word_frequencies(source,1)

    for keys,values in result.items():
#    print (keys)
        for keyword in found_words:
            if(keyword==keys):
                record=[]
                index+=1
                record.append(keys)
#                 print ("new row id",last_row_id)
                datetime_object = datetime.datetime.now()
                record.append(str(datetime_object))
                record.append(values)
#                print ("*"+record+"*")
                record.append(source)
                insert_data(record,con)

def retrieve_links(url,keywords,con,index):
    '''Accessing URLs within a resource'''
    page=requests.get(url)
    if page!=None:
        print ("success")
        soup = BeautifulSoup(page.text,'lxml')
        #print (soup)
        links = []
        for link in soup.find_all(attrs={'href': re.compile("http")}):
            links.append(link.get('href'))
        print(links)
        parse_info(links,keywords,con,index)
    else:
        print ("request unsucessfull")

def parse_info(links,keywords,con,index):
    '''Fetching data from URL, checking presence of defined keywords in it'''
    for page_url in links:
        content=requests.get(page_url)
        soup=BeautifulSoup(content.text,'lxml')
        txt=soup.text
        for word_pos in range(0,len(keywords)):
            #word=re.compile(word)
            word=keywords[word_pos][1]
            #print (word)
            datetime_object = datetime.datetime.now()
            #print("******")
            x=re.findall(word,txt,re.IGNORECASE)
            #print(len(x),word)
            record=[]
            index+=1
     #       record.append(index)
            record.append(word)
            record.append(datetime_object)
            record.append(len(x))
            record.append(page_url)
            insert_data(record,con)
      
    
con=sql_connection()
sql_table(con)

'''Set of keywords'''
keyword_data=[(1,'Wheat'),(2,'Corn'),(3,'Soybeans'),(4,'Soybean Meal'),(5,'Soybean Oil'),(6,'Oats'),(7,'Rough Rice'),(8,'Wheat'),(9,'Crude Oil'),(10,'Gasoline'),(11,'Natural Gas'),(12,'Ethanol'),(13,'Live Cattle'),(14,'Feeder Cattle'),(15,'Lean Hogs'),(16,'Gold'),(17,'Silver'),(18,'High Grade Copper'),(19,'Platinum'),(20,'Palladium'),(21,'SOFTS'),(22,'Cotton'),(23,'Orange juice'),(24,'Coffee'),(25,'Sugar'),(26,'Cocoa'),(27,'Lumber')]

'''Set of resources'''
resources_data=[(1,'CNBC Finance','https://www.cnbc.com/finance'),(2,'Market Watch','https://www.marketwatch.com/investing/futures'),(3,'Investing','https://www.investing.com'),(4,'Yahoo Finance','https://finance.yahoo.com')]

insert_table(con,keyword_data,resources_data)
index=0
scraping(con,resources_data,keyword_data,index)


for each_record_pos in range(0,len(resources_data)):
    url=resources_data[each_record_pos][2]
    index+=1
    retrieve_links(url,keyword_data,con,index)
con.close()
sqlite3_close()