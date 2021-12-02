# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE

**Task 07: Querying RDF(s)**
"""
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**
"""
from rdflib import RDFS, RDF

from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")

# RDFLIB
for subs, _, _ in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(f"[RDFLIB] SUBCLASSES: {subs}")

q = prepareQuery("""
    SELECT DISTINCT ?type
    WHERE{
        ?type rdfs:subClassOf ns:Person.
    }
""",
initNs={
    'ns': "http://somewhere#",
    'rdfs': "http://www.w3.org/2000/01/rdf-schema#"
})

for subs in g.query(q):
    print(f"[SPARQL] SUBCLASSES: {subs[0]}")

"""
**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
"""
# RDFLIB
print()
# Subclasses First

for subs, p1, o1 in g.triples((None, RDF.type, None)):
    for _ in g.triples((o1, RDFS.subClassOf, ns.Person)):
        print(f"[RDFLIB] INDIVIDUALS: {subs}")
# Actual Instances of Person
for subs in g.triples((None, RDF.type, ns.Person)):
    print(f"[RDFLIB] INDIVIDUALS: {subs[0]}")


# SPARQL 
q = prepareQuery("""
    SELECT DISTINCT ?person
    WHERE {
        ?person a ?type.
        ?type rdfs:subClassOf* ns:Person.
    }
""",
initNs={
    'ns': "http://somewhere#",
    'rdfs': "http://www.w3.org/2000/01/rdf-schema#"
})

for subs in g.query(q):
    print(f"[SPARQL] INDIVIDUALS: {subs[0]}")


"""
**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
"""

print()
# 
for subs, p1, o1 in g.triples((None, RDF.type, None)):
    for _ in g.triples((o1, RDFS.subClassOf, ns.Person)):
        for s, p, o in g.triples((subs, None, None)):
            print(f"[RDFLIB] ALL: {subs} {p} {o}")


# Actual Instances of Person
for subs, p1, o1 in g.triples((None, RDF.type, ns.Person)):
    for s, p, o in g.triples((subs, None, None)):
        print(f"[RDFLIB] ALL: {subs} {p} {o}")




q = prepareQuery("""
    SELECT DISTINCT ?person ?prop ?value
    WHERE {
        ?person a ?type.
        ?type rdfs:subClassOf* ns:Person.
        ?person ?prop ?value.
    }
""",
initNs={
    'ns': "http://somewhere#",
    'rdfs': "http://www.w3.org/2000/01/rdf-schema#"
})


for subs, prop, val in g.query(q):
    print(f"[SPARQL] ALL: {subs} {prop} {val}")
    
