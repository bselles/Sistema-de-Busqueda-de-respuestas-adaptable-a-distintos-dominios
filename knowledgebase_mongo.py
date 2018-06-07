#import psycopg2
import json
from pymongo import MongoClient, ASCENDING
from natural_language import Analysis
from bs4 import BeautifulSoup


def connect(db_name):
    try: 
        print('\n\nConnection to', db_name)
        db_info=''
        conn = psycopg2.connect(db_info) 
        print('Connection to', db_name, 'established')
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            conn.close()
            print('Database connection closed.')
        return None
    
def disconnect(conn):
    try:
        conn.close()
    except Exception as e:
        print(e)
        
        
        
def createDatabase(dataAmount):
    limit = ''
    try:
        limit = 'limit ' + str(int(dataAmount)/2) if int(dataAmount)>0 else ''
        print(limit)
    except:
        print('rompe')
        
    conn = connect('medwhat_articles_e4') 
    query_article_sections = """
        select article_sections.content
        from article_sections """+limit+""";"""
    
    query_search_engine_content_so = """
        select search_engine_content_so.content
        from search_engine_content_so """+limit+""";"""
        
    cur=conn.cursor()
    cur.execute(query_article_sections)
    data = []
    index = 0
    for result in cur.fetchall():
        tmp = {}
        tmp['content'] = str(list(result)[0])
        data.append(tmp)
        index = index + 1
    cur.execute(query_search_engine_content_so)
    for result in cur.fetchall():
        tmp = {}
        tmp['content'] = str(list(result)[0])
        data.append(tmp)
        index = index + 1
    disconnect(conn)
    client = MongoClient('')
    client.tfgchat.test.delete_many({})
    client.tfgchat.test.insert_many(data)
    

def getMostRelevantDocument(q):
    client = MongoClient('')
    query = ' '.join(q.content_words())
    client.tfgchat.test.create_index([('content', "text")])
    cursor = client.tfgchat.test.find_one({"$text":{"$search":query}},
                                  {"score":{"$meta":"textScore"}})
    return BeautifulSoup(cursor.get('content'), 'html.parser').get_text()

def retrieveDocument (q):
    #createDatabase(2000)
    return getMostRelevantDocument(q)



if __name__ == "__main__":
    q = Analysis("What is a heart attack?")
    print(retrieveDocument(q))