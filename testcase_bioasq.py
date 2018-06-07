from ground import Ground
from natural_language import Analysis
from natural_language import compose_answer
import json

from grafeno.transformers.interrogative import open as openQ
from grafeno.transformers.interrogative import closed


def response (q,answers, question_type):
    if question_type == openQ:
        if len(answers)==0:
            return "Sorry, I don't know the answer."
        else:
            return '\n'.join(compose_answer(q, a) for a in answers)
    else:
        #If its closed, answers will be a number counting the number of answers reached.
        if answers==0:
            return 'No'
        else:
            return 'Yes'

def do_tests(original_path, destination_path,type_filter='none'):
    json_file = json.load(open(original_path))
    all_tests = []
    errors = {}
    ground = Ground()
    
    for question in json_file['questions']:
        # Error Handling
        snipped_errors = ""
        question_errors = ""
        compose_answer_errors = False
        
        question_text = question['body']
        ideal_answer = question['ideal_answer']

        ground.teardown()

        for snippet in question['snippets']:
            snippet_text = snippet['text']
            try:
                ground.add_text(Analysis(snippet_text))
            except(KeyError):
                snipped_errors = snippet_text

        try:
            q = Analysis(question['body'])
            
            question_type=q.graph.question_type
            
            #If, because of the filter, we have to avoid this type of question, we go to the next for iteration.
            if(type_filter!='none' and type_filter!=question_type):
                continue
                
            print('------------------------------------')
            print('Question: ' + question_text)
            print('Question type: '+ question_type)
            print('Ideal answer: '+ ideal_answer[0])
            answers = ground.ask_question(q)
        except:
            question_errors = question['body']
            print('     Question errors: ' + question_errors)
        
        try:
            answers=response(q,answers,question_type)
        except:
            print('     Compose answer errors')
            compose_answer_errors = True
                
        print('Answer: ' + answers)

        all_tests.append({'question':question_text, 'answer': answers, 'ideal_answer':ideal_answer,
                          'snipped_errors':snipped_errors, 'question_errors':question_errors, 'compose_answer_errors':compose_answer_errors})
    
    full = {"questions":all_tests}
    
    dump = json.dumps(full)
    f = open(destination_path,"w")
    f.write(dump)
    f.close()