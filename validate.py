#!/usr/bin/env python
from rdflib.graph import Graph
from rdflib.namespace import Namespace,RDFS,RDF,FOAF,XSD,DC,OWL
import sys,re,os
#from IPython.core.display import display,HTML


if len(sys.argv)<2: 
    print "insert file name"
    raise Exception('no file name')

def textbox(text,color):
    display(HTML('<div><textarea style="background-color:{1};" cols="120" rows="20">{0}</textarea></div>'.format(text,color)))

color={'pass':'green','error':'red','warning':'yellow'}       
g=Graph()
g.parse(sys.argv[1])

files=[queryfile for queryfile in os.listdir('.') if re.match(r'rule.+\.sparql',queryfile) is not None]

try:
    for f in files:
        with open (f,'r') as query: sparql=(query.read())
        
        print "testing rule {0}".format(re.sub(r'rule.([\d]+).*',r'\1',f))
        qres=g.query(sparql,initNs=dict(foaf=FOAF,
                                           dct=Namespace("http://purl.org/dc/terms/"),
                                           spdx=Namespace("http://spdx.org/rdf/terms#")))
        print sparql
	if not len(qres): 
            print "pass"
        else:
            for r in qres: 
                result=[st.toPython() for st in r if st]
                print('{0} {1} class {2} ,rule message: {3}'.format(result[2],result[1],result[0],result[3]))
except Exception as e:
    print "{0} for \n{1}".format(e,sparql)

