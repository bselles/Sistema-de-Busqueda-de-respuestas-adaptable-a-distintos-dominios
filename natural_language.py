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

'''
    Class that represents an spell-corrected and analyzed text which is going to be used by the system.
    From this analyzed text we can create cypher querys, get the most relevant terms, etc.    
'''
class Analysis:

    def __init__ (self, text, superficial=False,autocorrect=True):
        # Corrects posible misspelled words in the queries
        if autocorrect:
            self.text = correct_phrase(text)
        else:
            self.text=text
        
        if superficial:
            # Parses the query without generating the semantic graph
            self.parse = nlp(self.text)
        else:
            # Deeply parses the query generating the semantic graph
            self.graph = CG(transformer=semantic_analyzer,text=self.text)
            self.parse = self.graph.spacy_parse
    
    #Returns the similarity between this object and another of its same type.
    def similarity (self, other):
        return self.parse.similarity(other.parse)
        
    #Returns the most relevant terms from the analyzed text represented by this object.
    def content_words (self):
        return [tok.lemma_ for tok in self.parse if not (tok.is_stop or tok.is_punct)]
        
    # Generates MATCH queries to solve the question introduce by the user
    def cypher_query (self, ground_id):
        if self.graph.question_type==closed:
            return self.graph.linearize(linearizer=cypher_closed_linearizer,
                                        linearizer_args={ 'cypher_extra_params': {'ground_id': ground_id }})
        elif self.graph.question_type == open:
            return self.graph.linearize(linearizer=cypher_open_linearizer,
                                        linearizer_args={ 'cypher_extra_params': {'ground_id': ground_id }})
    
    # Generates CREATE queries to add the information to the NEO4J graph database
    def cypher_create (self, ground_id):
        return self.graph.linearize(linearizer=cypher_create_linearizer,
                                    linearizer_args={ 'cypher_extra_params': {'ground_id': ground_id }})
    
# Corrects the misspelled words in the sentences
def correct_phrase(text):
    words = text.split()
    for i in range(len(words)):
        words[i] = spell(words[i])
    return ' '.join(words)
    
# Generates the natural language sentences from semantic graphs
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
