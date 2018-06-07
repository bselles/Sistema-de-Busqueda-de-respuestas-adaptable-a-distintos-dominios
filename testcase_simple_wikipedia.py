import json 
import requests
from bs4 import BeautifulSoup
from knowledgebase_wiki import retrieveDocument, wikiSearch
from ground import Ground 
from natural_language import Analysis, compose_answer
from grafeno.transformers.interrogative import open as openQ
from grafeno.transformers.interrogative import closed


def load(questions_file, answers_file, result_file):
    json_sw = {}
    json_sw['questions'] = []

    url = 'https://simple.wikipedia.org/w/api.php'
    with open(questions_file, 'r') as q_file:
        with open(answers_file, 'r') as a_file:
            questions = q_file.read().splitlines()
            answers = a_file.read().splitlines()
            for question in questions:
                data = wikiSearch(question.split())
                responses = json.loads(data.text)['query']['search']
                answer = BeautifulSoup(responses[0]['snippet'], 'html.parser')

                snippets = list()
                for response in responses:
                    snippet = BeautifulSoup(response['snippet'], 'html.parser').get_text()
                    snippets.append({'text': snippet})

                json_sw['questions'].append({'body':question,
                                             'ideal_answer':answers.pop(0),
                                             'snippets':snippets})

    with open(result_file,'w') as file:
        json.dump(json_sw, file)
        
        
def response(data_file):
    with open(data_file,'r') as file:
        data = json.load(file)
        #print(json.dumps(data, indent=4, sort_keys=True))
        ground = Ground()
        for i in data['questions']:
            question = Analysis(i['body'])
            question_type=question.graph.question_type
            doc = Analysis(retrieveDocument(question))
            ground.teardown()
            ground.add_text(doc)
            answers = ground.ask_question(question)
            print('------------------------------------')
            print('Question: ' + i['body'])
            print('Question type: '+ question_type)
            print('Ideal answer: ', i['ideal_answer'])
            if(len(answers)==0): print("Answer: Sorry, I don't know the answer.")
            else:
                print('Answer: ', '\n'.join(compose_answer(question, a) for a in answers))