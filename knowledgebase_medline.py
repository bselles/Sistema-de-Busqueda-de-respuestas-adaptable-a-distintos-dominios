from natural_language import Analysis
import requests
from bs4 import BeautifulSoup

def medlineSearch (terms):
    query = {'db':'healthTopics','term':'title:'+'+OR+'.join(terms)}
    return requests.get("https://wsearch.nlm.nih.gov/ws/query", query)

def rankDocument (doc, q):
    titly = doc.find_all("content", attrs={"name": ["title","altTitle"]})
    hl = 0 # count of terms highlited by search engine
    sim = 0 # query-defined similarity with the titles
    for t in titly: # We search for the max scores from all the title entries
        c = BeautifulSoup(t.get_text(), "html.parser")
        hl = max(hl, len(c.find_all("span")))
        sim = max(sim, q.similarity(Analysis(c.get_text(), superficial=True)))
    return hl + sim

def getMostRelevantDocument (response, q):
    parsed = BeautifulSoup(response.text, "html.parser")
    docs = parsed.find_all('document')
    doc = max(docs, key=lambda d: rankDocument(d, q))
    html = doc.find("content", attrs={"name": "FullSummary"}).get_text()
    return BeautifulSoup(html, "html.parser").get_text(" ")

def retrieveDocument (q):
    r = medlineSearch(q.content_words())
    doc = getMostRelevantDocument(r, q)
    return ' '.join(doc.split())


if __name__ == "__main__":
    q = Analysis("What are the causes of blood infection?")
    print(q.content_words())

    r = medlineSearch(q.content_words())
    print("{} -> {}".format(r.url, r.status_code))

    doc = getMostRelevantDocument(r, q)
    print(doc)

    print(retrieveDocument(Analysis("What are the causes of a heart attack?")))