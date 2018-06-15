import psycopg2
import json
from pymongo import MongoClient, ASCENDING
from natural_language import Analysis
from bs4 import BeautifulSoup


def connect(db_name):
    """
    Establishes the connection with the database.

    This method establishes the connection with the
    database using psycopg2. If the connection fails
    return an exception and print a error log, otherwise
    it creates a database session and return a new
    connection object.

    Parameters
    ----------
    db_name : string
        Name of the database used

    Returns
    -------
    connection
        Connection object of the database

    """

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
    """
    Closes the connection with the database.

    This method closes the connection with the
    database. If it fails print a error log.

    Parameters
    ----------
    conn : connection
        Connection object of the database

    """

    try:
        conn.close()
    except Exception as e:
        print(e)
        
        
        
def createDatabase(dataAmount):
    """
    Fills the database with information.

    This method creates a NoSQL database from a SQL.
    For it uses 2 tables of the SQL database and takes
    information from both. If the parameters are invalid
    it take all the information from the database.

    Parameters
    ----------
    dataAmount : int
        Amount of data to be load into the NoSQL database

    """

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
    """
    Takes the most important document based on input parameters.

    This method takes the most important document of
    a NoSQL database based on the input params content.
    For that creates an index in the database based on
    the content of all documents. Once this is done
    makes a query with the input terms and return a text
    chain with the result.

    Parameters
    ----------
    q : list(string)
        List of relevant term to used in the search query

    Returns
    -------
    string
        Most relevant information based on the input

    """

    client = MongoClient('')
    query = ' '.join(q.content_words())
    client.tfgchat.test.create_index([('content', "text")])
    cursor = client.tfgchat.test.find_one({"$text":{"$search":query}},
                                  {"score":{"$meta":"textScore"}})
    return BeautifulSoup(cursor.get('content'), 'html.parser').get_text()

def retrieveDocument (q):
    """
    Creates a NoSQL database and return the most relevant
    document on it.

    This method creates a NoQSL database with an arbitrary
    amount of data.

    Parameters
    ----------
    q : list(string)
        List of relevant term to used in the search query

    Returns
    -------
    string
        Most relevant information based on the input

    """

    createDatabase(2000)
    return getMostRelevantDocument(q)



if __name__ == "__main__":
    q = Analysis("What is a heart attack?")
    print(retrieveDocument(q))