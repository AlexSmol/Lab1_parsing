import requests
from bs4 import BeautifulSoup
import sqlite3




site='https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=1&room2=1'

Apart_link=[]
Rooms=[1]#,2,3,4,5,6

def page_link(url):
    start_url='https://www.cian.ru'
    r = requests.get(url)
    bs_pars = BeautifulSoup(r.content, 'html.parser')
    #print(bs_pars.find_all(class_="a10a3f92e9--img-link-wrapper--wi8vG"))
    href_url=list(set([i['href'] for i in bs_pars.find_all(href=True) if 'https://www.cian.ru/sale/flat/' in i['href']]))
    return href_url

#print(page_link(site))
#print('Amount =',len(page_link(site)))

def parsing_page(url):
    
    Information=[] # storage massive

    r = requests.get(url, stream=True) # input get
    bs_pars = BeautifulSoup(r.content, 'html.parser') # processing get

    ID=url.replace('https://www.cian.ru/sale/flat/','').replace('/','')
    Name=[i.text for i in bs_pars.find_all(class_="a10a3f92e9--title--UEAG3")]
    Area=[i.text.replace('\xa0м²','') for i in bs_pars.find_all(class_="a10a3f92e9--info-value--bm3DC")]
    Price=[i.text.replace('\xa0', ' ').replace('₽','').replace(' ','') for i in bs_pars.find_all(itemprop='price')] # pulling out the price
    Price_currency=[i['content'] for i in bs_pars.find_all(itemprop='priceCurrency')] # pulling currency
    Phone_Number=[i.text for i in bs_pars.find_all(class_="a10a3f92e9--phone--_OimW")]
    address=[i for i in bs_pars.find_all(itemprop='name')]
    #Descriptor=[i.text.replace('\n',' ') for i in bs_pars.find_all(itemprop="description")]
    

    Information=[ID,Name[0],address[-1]['content'],Area[0],Price[0],Price_currency[0],Phone_Number,url]
    return Information

def parsing_offer(var):
    for room in Rooms:
        for page in range(1,2):
            temporary_link='https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p='+str(page)+'&region=1&room2='+str(room)
            temporary_var=[var.append(i) for i in page_link(temporary_link)]
            print('Процесс по странице: '+str(page)+' из 54; Процесс по количеству комнат: '+str(room)+' из 6; Найдено: '+str(len(page_link(temporary_link))))
            del(temporary_var)
        parsing
    print('Число записей',len(var))
    Apart_link=len(set(var))
    print('Число уникальных записей',len(var))

#parsing_offer(Apart_link)

print(parsing_page('https://www.cian.ru/sale/flat/267715333/')[2])


def create_table(connect_db):
    connect_db.execute('''CREATE TABLE Flat ( 
                       ID integer primary key not null unique,
                       Name_Offer text,
                       Count_room integer,
                       Adress text,
                       Area real,
                       Price integer,
                       Price_Currency text,
                       Phone_Number text,
                       Link text not null unique);''')
                       

def insert_table(connect_db,massiv,count_room):
    string_massiv="INSERT INTO Flat VALUES ("+str(massiv[0])+",'"+str(massiv[1])+"',"+str(count_room)+","+str(massiv[2])+","+str(massiv[3])+","+str(massiv[4])+","+str(massiv[5])+","+str(massiv[6])+","+str(massiv[7])+")"
    connect_db.execute(string_massiv)
    return

def InsertTable(CDB,massive):
    inform=get_inform(massive)
    string_for_recording="'"+massive[-20:-1]+"',"+inform[0]+",'"+inform[1]+"','"+inform[2]+"','"+inform[3]+"','"+massive+"'"

    print(string_for_recording)
    CDB.execute("INSERT INTO AutoRu VALUES ("+string_for_recording+")")



def Work_with_table():
    con=sqlite3.connect(r'Cian/Cian_inform.db')
    cur = con.cursor()
    

