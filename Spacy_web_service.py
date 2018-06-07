'''
Spacy web service.

Usage:
  Spacy_web_service.py [--app=<application>] [--server=<adapter>] [--host=<h>] [--port=<p>] [--reloader=<r>] [--interval=<i>] [--quiet=<q>] [--options=<o>] [--debug=<d>]
  Spacy_web_service.py (-h | --help)

Options:
  -h --help              Show this screen.
  --version              Show version.
  --app=<application>    WSGI application or target string supported by load_app().[default: default_app()])
  --server=<adapter>     Server adapter to use. See server_names keys for valid names or pass a ServerAdapter subclass. [default: wsgiref]
  --host=<h>             Server address to bind to. Pass 0.0.0.0 to listens on all interfaces including the external one. [default: 127.0.0.1]
  --port=<p>             Server port to bind to. Values below 1024 require root privileges. [default: 8080]
  --reloader=<r>         Start auto-reloading server? [default: False]
  --interval=<in>        Auto-reloader interval in seconds [default: 1]
  --quiet=<q>            Suppress output to stdout and stderr? [default: False]
  --options=<o>          Options passed to the server adapter.
  --debug=<d>            Debug mode. [default: False]

'''
from docopt import docopt
from bottle import run, get, post, request
import spacy

'''
    GLOBAL VARIABLES
'''
lang = {}

'''
    This is a method that works like an Api Rest.
    It receives a json with the text you want to parse and a language.
    Returns a json with two lists, one of edges and one of nodes, as well as
    all the attributes that may be useful.
'''
@post('/spacy/parse')
def parse():
    text = request.json.get('text')
    local_lang = request.json.get('lang')
    
    load = lang.get(local_lang)
    if load != None:
        nlp = load
    else:
        try:
            nlp = spacy.load(local_lang)
            lang.update({local_lang:nlp})
        except:
            return {}
    
    try:
        parse = nlp(text)
    except:
        return {}
    
    sents = []
    for tree in parse.sents:
        nodes = []
        edges = []
        root = tree.root.i
        for word in tree:
            if word.i != word.left_edge.i:
                edges.append({'parent': word.i, 'child':word.left_edge.i, 'dep':word.left_edge.dep_})
            if word.i != word.right_edge.i:
                edges.append({'parent': word.i, 'child':word.right_edge.i, 'dep':word.right_edge.dep_})
            
            nodes_dict = {'text':word.text}
            nodes_dict.update({'text_with_ws':word.text_with_ws})
            nodes_dict.update({'whitespace_':word.whitespace_})
            nodes_dict.update({'orth':word.orth})
            nodes_dict.update({'orth_':word.orth_})
            nodes_dict.update({'head':word.head.ent_id})
            nodes_dict.update({'left_edge':word.left_edge.i})
            nodes_dict.update({'right_edge':word.right_edge.i})
            nodes_dict.update({'i':word.i})                         # -> This is what I'm using as id
            nodes_dict.update({'ent_type':word.ent_type})
            nodes_dict.update({'ent_type_':word.ent_type_})
            nodes_dict.update({'ent_iob':word.ent_iob})
            nodes_dict.update({'ent_iob_':word.ent_iob_})
            nodes_dict.update({'ent_id':word.ent_id})
            nodes_dict.update({'ent_id_':word.ent_id_})
            nodes_dict.update({'lemma':word.lemma})
            nodes_dict.update({'lemma_':word.lemma_})
            nodes_dict.update({'norm':word.norm})
            nodes_dict.update({'norm_':word.norm_})
            nodes_dict.update({'lower':word.lower})
            nodes_dict.update({'lower_':word.lower_})
            nodes_dict.update({'shape':word.shape})
            nodes_dict.update({'shape_':word.shape_})
            nodes_dict.update({'prefix':word.prefix})
            nodes_dict.update({'prefix_':word.prefix_})
            nodes_dict.update({'suffix':word.suffix})
            nodes_dict.update({'suffix_':word.suffix_})
            nodes_dict.update({'is_alpha':word.is_alpha})
            nodes_dict.update({'is_ascii':word.is_ascii})
            nodes_dict.update({'is_digit':word.is_digit})
            nodes_dict.update({'is_lower':word.is_lower})
            #nodes_dict.update({'is_upper':word.is_upper})
            nodes_dict.update({'is_title':word.is_title})
            nodes_dict.update({'is_punct':word.is_punct})
            nodes_dict.update({'is_left_punct':word.is_left_punct})
            nodes_dict.update({'is_right_punct':word.is_right_punct})
            nodes_dict.update({'is_space':word.is_space})
            nodes_dict.update({'is_bracket':word.is_bracket})
            nodes_dict.update({'is_quote':word.is_quote})
            nodes_dict.update({'like_url':word.like_url})
            nodes_dict.update({'like_num':word.like_num})
            nodes_dict.update({'like_email':word.like_email})
            nodes_dict.update({'is_oov':word.is_oov})
            nodes_dict.update({'is_stop':word.is_stop})
            nodes_dict.update({'pos':word.pos})
            nodes_dict.update({'pos_':word.pos_})
            nodes_dict.update({'tag':word.tag})
            nodes_dict.update({'tag_':word.tag_})
            nodes_dict.update({'dep':word.dep})
            nodes_dict.update({'dep_':word.dep_})
            nodes_dict.update({'lang':word.lang})
            nodes_dict.update({'lang_':word.lang_})
            nodes_dict.update({'prob':word.prob})
            nodes_dict.update({'idx':word.idx})
            nodes_dict.update({'sentiment':word.sentiment})
            nodes_dict.update({'lex_id':word.lex_id})
            nodes_dict.update({'rank':word.rank})
            nodes_dict.update({'cluster':word.cluster})
            nodes.append(nodes_dict)
        
        full = dict(nodes=nodes)
        full.update(dict(edges=edges))
        full.update({'root':root})
    
        # I join all the dictionaries in one
        full.update({'start':tree.start})
        full.update({'end':tree.end})
        full.update({'start_char':tree.start_char})
        full.update({'end_char':tree.end_char})
        full.update({'text':tree.text})
        full.update({'text_with_ws':tree.text_with_ws})
        #full.update({'orth':tree.orth}) # v2.0
        full.update({'orth_':tree.orth_})
        full.update({'label':tree.label})
        full.update({'label':tree.label_})
        full.update({'lemma_':tree.lemma_})
        full.update({'ent_id':tree.ent_id})
        full.update({'ent_id_':tree.ent_id_})
        full.update({'sentiment':tree.sentiment})
        #vocab = tree.doc.vocab
        #full.update({'vocab':[{'strings':vocab.strings.string},{'vectors_length':vocab.length}]})
        sents.append(full)
    
    return dict(data=sents)

'''
    Create a natural language processing object in the language indicated by parameter
'''
@get('/spacy/set_language/<param>')
def set_language(param):
    # If it is already preprocessed, it does not repeat the job
    global lang
    
    if param == lang:
        return {'data':True}
    
    try:
        global nlp 
        nlp = spacy.load(param)
    except:
        return {'data':False}
    
    lang = param;
    
    return {'data':True}

'''
    Main
'''
if __name__ == "__main__":
    arguments = docopt(__doc__)
    
    # We can not specify the app parameter
    run(server=arguments.get('--server'),
        host=arguments.get('--host'), port=arguments.get('--port'),
        reloader=arguments.get('--reloader')=='True', interval=int(arguments.get('--interval')),
        quiet=arguments.get('--quiet')=='True',debug=arguments.get('--debug')=='True')