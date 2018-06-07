from grafeno import Graph as CG, transformers, linearizers
from grafeno.operations.graft import graft
import spacy
from grafeno.transformers.interrogative import open, closed

semantic_analyzer = transformers.get_pipeline([ 'spacy_parse', 'pos_extract', 'pronouns',
	'nouns', 'thematic', 'phrasal', 'genitive', 'prepositions', 'adjectives', 'adverbs',
	'negation', 'interrogative', 'copula', 'lenient' ])
cypher_open_linearizer = linearizers.get_pipeline(['cypher_open_question'])
cypher_closed_linearizer = linearizers.get_pipeline(['cypher_closed_question'])

cypher_create_linearizer = linearizers.get_pipeline(['cypher_create'])
nlg = linearizers.get_pipeline(['simplenlg'])

from autocorrect import spell

global nlp
nlp = spacy.load('en')

class Analysis:

    def __init__ (self, text, superficial=False,autocorrect=True):
       
        if autocorrect:
            self.text = correct_phrase(text)
        else:
            self.text=text
    
        if superficial:
            self.parse = nlp(self.text)
        else:
            self.graph = CG(transformer=semantic_analyzer,text=self.text)
            self.parse = self.graph.spacy_parse
        
    def similarity (self, other):
        return self.parse.similarity(other.parse)
        
    def content_words (self):
        return [tok.lemma_ for tok in self.parse if not (tok.is_stop or tok.is_punct)]
        
    def cypher_query (self, ground_id):
        if self.graph.question_type==closed:
            return self.graph.linearize(linearizer=cypher_closed_linearizer,
                                        linearizer_args={ 'cypher_extra_params': {'ground_id': ground_id }})
        elif self.graph.question_type == open:
            return self.graph.linearize(linearizer=cypher_open_linearizer,
                                        linearizer_args={ 'cypher_extra_params': {'ground_id': ground_id }})
    
    def cypher_create (self, ground_id):
        return self.graph.linearize(linearizer=cypher_create_linearizer,
                                    linearizer_args={ 'cypher_extra_params': {'ground_id': ground_id }})
    
def correct_phrase(text):
    words = text.split()
    for i in range(len(words)):
        words[i] = spell(words[i])
    return ' '.join(words)
    
def compose_answer (question, answer_graph):
    g = CG(original=question.graph)
    graft(g, question.graph.questions[0], answer_graph, answer_graph.roots[0])
    return(g.linearize(linearizer=nlg))

if __name__ == "__main__":
    question = Analysis("What are the causes of heart attack?")
    print(question.similarity(Analysis("The most common clause of heart attack is a clogging of the arteries.", superficial=True)))
    print(question.similarity(Analysis("The most common clause of lung cancer is excessive smoking.", superficial=True)))
    print(question.content_words())
    aux=question.content_words()
    print(Analysis("cause heart attack").similarity(Analysis("cause heart attack")))
    print(question.cypher_create(1))
    print(question.cypher_query(1))
    answer = Analysis("A clogging of the arteries")
    print(compose_answer(question, answer.graph))
