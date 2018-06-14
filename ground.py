import yaml
from neo4j.v1 import GraphDatabase, basic_auth
from grafeno import Graph as CG
from grafeno.linearizers.cypher_query import reconstruct_graphs


global ground_id_counter, driver
ground_id_counter = 0
params = yaml.load(open('config.yml'))
driver = GraphDatabase.driver(params['neo4j']['uri'], auth=(params['neo4j']['user'], params['neo4j']['password']))

from grafeno.transformers.interrogative import open, closed



def neo4j_multi_query (query):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for statement in query.split('\n'):
                tx.run(statement)
                
'''
    Manages the interaction between the user and the knowledge base.
    Allows the user to add information to the knowledge base and queries this
    in order to answer the questions.
'''
class Ground:
    
    def __init__ (self):
        #Is used to distinguish between different conversations User-Machine
        global ground_id_counter
        self.ground_id = ground_id_counter
        ground_id_counter += 1
    
    # Called when adding information to the knowledge base
    def add_text (self, text):
        query = text.cypher_create(self.ground_id)
        neo4j_multi_query(query)
    
    # Called when solving a query introduce by the user
    def ask_question (self, text):
        query = text.cypher_query(self.ground_id)
        r = driver.session().run(query)
        
        #Depending on the question_type, we will return a number or a graph.
        if text.graph.question_type == closed :
            for record in r.records():
                return record['count(*)']
        elif text.graph.question_type == open: 
            return reconstruct_graphs(r)
        
    # Called when clearing the information contained in the knowledge base
    def teardown (self):
        driver.session().run("MATCH (u) WHERE u.ground_id = {ground_id} DETACH DELETE u;", **{'ground_id':self.ground_id})
        
def test_init():
    global Analysis, nlg
    
    import nbimporter
    from natural_language import Analysis
    
    from grafeno import linearizers
    nlg = linearizers.get_pipeline(['node_edges'])


# Test case showing the behavior of Ground class
if __name__ == "__main__":
    
    test_init()
    ground = Ground()
    ground.teardown()
    ground.add_text(Analysis("John loves Mary. John loves very cute dogs. Peter hates Susan. Susan loves John. Paul loves Joana. Joana loves Paul."))
    answers = ground.ask_question(Analysis("Who loves John"))
    for answer in answers:
        print(answer.linearize(linearizer=nlg))

    print('##########################################################')
    answers = ground.ask_question(Analysis("John loves who"))
    for answer in answers:
        print(answer.linearize(linearizer=nlg))
