import csv
from tkinter.messagebox import NO
import requests
from bs4 import BeautifulSoup
from os import path

class DbObject:
    def __init__(self, title, desc, keywords, url):
        self.title = title
        self.desc = desc
        self.keywords = keywords
        self.url = url

def isNotBlank (myString):
    if myString and myString.strip():
        return True
    return False

def getDataFromUrl(url):
    collected_data = {'url': url, 'title': None, 'description': None, 'keywords': None}
    try:
        try:
            r = requests.get(url, timeout=5)
        except Exception:
            return None

        if r.status_code == 200:
            # print("Url: "+ str(url) + " -- Status code 200")

            # Se puede usar BeautifulSoap u otra librería que parsee la metadata de los docuementos HTML.
            source = requests.get(url).text
            # print("Parsing...")
            soup = BeautifulSoup(source, features='html.parser')
            # Se otienes las etiquetas meta
            # print("Finding metadata...")
            meta = soup.find("meta")
                
            if soup.find('meta', {"name":"title"}):
                title = soup.find("meta", {'name': "title"})["content"]
                # print("Url: " + url + "\n Title: " + str(title))
            elif soup.find_all('title'):
                title = soup.find('title').text
                
            if soup.find('meta', {"name":"description"}):
                description = soup.find("meta", {'name': "description"})["content"]
                # print("Url: " + url + " \n Desc: " + str(description))

            keywords = None

            if soup.find('meta', {"name":"keywords"}):
                keywords = soup.find("meta", {'name': "keywords"})["content"]
                # print("Url: " + url + "\n Keywords: " + str(keywords))   
            
            if keywords is None:
                    print("Exception: No keywords")
                    return None

            try:
                # title = title.get_text().replace("\n","") if title else None
                # title = title.replace("\r","") if title else None
                # title = title.replace("\t","") if title else None
                collected_data['title'] = title
                collected_data['description'] = description
                collected_data['keywords'] = keywords
            except Exception:
                print("Warning - Exception line 58\n")
                return None 

            if collected_data['keywords'] is None:
                    return None
            return collected_data

    except Exception:
        return None
          
    return None

def writeInitSQl(object):
    file = open("init.sql", "w")
    file.write("CREATE TABLE paginas(Id INT, title text, description text, keywords text, url text);")
    counter = 1
    for value in object:
        insert = "INSERT INTO paginas(Id, title, description, keywords, url) VALUES(" + str(counter) + ",'" + value.title + "','" + value.desc + "','" + value.keywords + "','" + value.url + "');\n"
        file.write(insert)
        counter += 1

if path.exists("init.sql"):
    print("\n\n------Listo------\n\n")
    pass
else:
    file = open("querylog8.txt", "r")

    df = csv.reader(file, delimiter="\t")
    counter = 0
    urlsVisitadas = []
    dbObjects = []

    for row in df:
        url = row[4]

        if isNotBlank(url):
            if url in urlsVisitadas:
                continue

            urlsVisitadas.append(url)
            data = getDataFromUrl(row[4])
            
            # print("Getting data from: " + str(row[4]))
            if data is not None:
                print(f'[{counter}] {data["url"]}\n Title: {repr(data["title"])}\n Description: {repr(data["description"])}\n Keywords: {repr(data["keywords"])}')
                dataModel = DbObject(str(data["title"]), str(data["description"]), str(data["keywords"]), str(data["url"]))
                dbObjects.append(dataModel)
                counter += 1
        
        if counter > 100:
            print("\n\n------Listo------\n\n")
            break

    writeInitSQl(dbObjects)    
    
# while counter < 20:
#     df.
#     counter += 1
# print(df.readline().strip())
# print(df.readline().strip())
# print(df.readline().strip())

