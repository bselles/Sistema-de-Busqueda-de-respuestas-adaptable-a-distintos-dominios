from ground import Ground
from natural_language import Analysis
from natural_language import compose_answer
import json

from grafeno.transformers.interrogative import open as openQ
from grafeno.transformers.interrogative import closed

# Returns the answer depending on the type of question
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

'''
    Loads the JSON file containing the test cases and executes each of them using the
    corresponding resources.
    Each test case is composed by a query, some snippets and some ideal answers.
'''
def do_tests(original_path, destination_path,type_filter='none'):
    json_file = json.load(open(original_path))
    all_tests = []
    errors = {}
    # We create a single Ground
    ground = Ground()
    
    for question in json_file['questions']:
        # Error Handling
        snipped_errors = ""
        question_errors = ""
        compose_answer_errors = False
        
        question_text = question['body']
        ideal_answer = question['ideal_answer']

        # Clears the Ground
        ground.teardown()

        # Adds all the snippets to the current knowledge base
        for snippet in question['snippets']:
            snippet_text = snippet['text']
            try:
                ground.add_text(Analysis(snippet_text))
            except(KeyError):
                snipped_errors = snippet_text

        try:
            # Analyzes the query
            q = Analysis(question['body'])
            
            question_type=q.graph.question_type
            
            # If we have to avoid this type of question due to the filter, we move to the next for iteration
            if(type_filter!='none' and type_filter!=question_type):
                continue
                
            print('------------------------------------')
            print('Question: ' + question_text)
            print('Question type: '+ question_type)
            print('Ideal answer: '+ ideal_answer[0])
            
            # We ask a question to the current knowledge base
            answers = ground.ask_question(q)
        except:
            question_errors = question['body']
            print('     Question errors: ' + question_errors)
        
        try:
            # Translates the answer into a natural language sentence
            answers=response(q,answers,question_type)
        except:
            print('     Compose answer errors')
            compose_answer_errors = True
                
        print('Answer: ' + answers)
        
        # We collect all the relevant information
        all_tests.append({'question':question_text, 'answer': answers, 'ideal_answer':ideal_answer,
                          'snipped_errors':snipped_errors, 'question_errors':question_errors,
                          'compose_answer_errors':compose_answer_errors})
    
    # We collect all the questions
    full = {"questions":all_tests}
    
    # We saved all the questions into the specified file
    dump = json.dumps(full)
    f = open(destination_path,"w")
    f.write(dump)
    f.close()