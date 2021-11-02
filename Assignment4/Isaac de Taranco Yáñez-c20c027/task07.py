# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OR_uGP3noMh7dyeF0LnbosGKg5EgdxMG

**Task 07: Querying RDF(s)**
"""

!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

for s,p,o in g:
  print(s,p,o)

from rdflib.plugins.sparql import prepareQuery
#SPARQL
print("SPARQL")
ns = Namespace("http://somewhere#")
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdfs:subClassOf ns:Person. 
  }
  ''',
  initNs = {"rdfs":RDFS, "ns":ns}
)

for r in g.query(q1):
  print(r.Subject)

#RDFLib
print("RDFLib")
subclasses = g.triples((None, RDFS.subClassOf, ns.Person))
for s,p,o in subclasses:
  print(s)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

#SPARQL
print("SPARQL")
q2 = prepareQuery('''
  SELECT ?Subject WHERE { 

    {?Subject rdf:type ns:Person} UNION 
    {?Subject rdf:type ?tipo.
    ?tipo rdfs:subClassOf ns:Person}
  }
  ''',
  initNs = {"rdf":RDF, "ns":ns,"rdfs":RDFS}
)

# Visualize the results
for r in g.query(q2):
  print(r.Subject)

#RDFLib
print("RDFLib")
individuos1 = g.triples((None, RDF.type, ns.Person))
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  individuos2 = g.triples((None, RDF.type, s))
# Visualize the results
for s, p, o in individuos1:
  print(s)
for s, p, o in individuos2:
  print(s)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

#SPARQL
print("SPARQL")
q2 = prepareQuery('''
  SELECT ?Subject ?pred ?obj WHERE { 

    {?Subject rdf:type ns:Person} UNION 
    {?Subject rdf:type ?tipo.
    ?tipo rdfs:subClassOf ns:Person}

    ?Subject ?pred ?obj
  }
  ''',
  initNs = {"rdf":RDF, "ns":ns,"rdfs":RDFS}
)
# Visualize the results
for r in g.query(q2):
  print(r.Subject, r.pred, r.obj)

#RDFLib
print("RDFLib")
individuals1 = g.triples((None, RDF.type, ns.Person))
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  individuals2 = g.triples((None, RDF.type, s))

# Visualize the results
for s, p, o in individuals1:
  for s1, p1, o1 in g.triples((s, None, None)):
    print(s1,p1,o1)

for s, p, o in individuals2:
    for s1, p1, o1 in g.triples((s, None, None)):
      print(s1,p1,o1)