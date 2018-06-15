from natural_language import Analysis
from bs4 import BeautifulSoup
import requests
import json

'''
   Using the most relevant terms of the query introduced 
   by the user, it looks for different articles or 
   documents in which appears this terms  
'''
def wikiSearch (terms):
    query = {'action':'query','list':'search',
             'srwhat':'text','srsearch':' '.join(terms),
             'format':'json'
            }
    return requests.get("https://simple.wikipedia.org/w/api.php", query)


'''
    Using a page identifier (parameter 'pageId') from a Simple Wikipedia
    article, it retrieves this article.
'''
def wikiRetrieve (pageId):
    query = {'action':'parse','format':'json',
             'prop':'text',
             'pageid':pageId,
            }
    return requests.get("https://simple.wikipedia.org/w/api.php", query)

'''
    It analyzes a document or an article (parameter 'result')
    to get how good is it to response a certain question (parameter 'q'). 
'''
def rankResult (result, q):
    title_similarity = q.similarity(Analysis(result['title'], superficial=True))
    snippet = BeautifulSoup(result['snippet'], 'html.parser')
    matches = snippet.find_all('span', attrs={"class": "searchmatch"})
    match_score = len(set(m.get_text() for m in matches))
    #print('{}: {}+{}'.format(result['title'], title_similarity, match_score))
    title_weight = 1
    match_weight = 0.1
    return title_weight * title_similarity + match_weight * match_score


'''
    Using the documents retrieved (parameter 'response') and the analysis of the question introduced
    by the user (parameter 'q'), it gets the most relevant documents, the ones which have a 
    bigger probability to contain the response to the question.
'''

def getMostRelevantDocument (response, q):
    results = json.loads(response.text)['query']['search']
    best_result = max(results, key=lambda r: rankResult(r, q))
    page = wikiRetrieve(best_result['pageid'])
    content = BeautifulSoup(json.loads(page.text)['parse']['text']['*'], 'html.parser')
    return ' '.join(p.get_text() for p in content.find_all('p'))

'''
    Retrieves different documents which can contain the response to 
    question introduced by the user.
    To do it, it uses the result of the analysis of this question (parameter q).
'''
def retrieveDocument (q):
    r = wikiSearch(q.content_words())
    doc = getMostRelevantDocument(r, q)
    return ' '.join(doc.split())

if __name__ == "__main__":
    q = Analysis("What is the internet of things?")
    print(q.content_words())

    r = wikiSearch(q.content_words())
    print("{} -> {}".format(r.url, r.status_code))

    results = json.loads(r.text)['query']['search']
    print([(r['title'], r['snippet']) for r in results])

    page = wikiRetrieve(results[0]['pageid'])
    print(json.loads(page.text)['parse']['text']['*'])

    doc = getMostRelevantDocument(r, q)
    print(doc) 

    print(retrieveDocument(Analysis("What is a heart attack?")))
