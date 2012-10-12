#!/usr/bin/env python

"""hisco2rdf.py: An RDF graph generator for the HISCO occupation system."""

import csv
from xlrd import open_workbook
from rdflib import ConjunctiveGraph, Namespace, Literal, RDF, RDFS, BNode, URIRef

hiBook = open_workbook('data/HISCO.xls', formatting_info=True)
hiSheet = hiBook.sheet_by_index(0)

namespaces = {
    'd2s':Namespace('http://www.data2semantics.org/data/'),
    'cpm':Namespace('http://cedar-project.nl/harmonization/municipalities/'),
    'cpv':Namespace('http://cedar-project.nl/harmonization/variables/'),
    'cpo':Namespace('http://cedar-project.nl/harmonization/occupations/'),
    'rdfs':Namespace('http://www.w3.org/2000/01/rdf-schema#'),
}

graph = ConjunctiveGraph()
for namespace in namespaces:
    graph.namespace_manager.bind(namespace, namespaces[namespace])


## Cols to read: [0,1] Rows to read: [2:53216]
hiCodes = []
for i in range(1,53216):
    print i
    graph.add((
            namespaces['cpo'][str(hiSheet.cell(i,1).value)],
            RDF.type,
            namespaces['cpo']['HISCOOccupation']
            ))
    graph.add((
            namespaces['cpo'][str(hiSheet.cell(i,1).value)],
            namespaces['cpo']['hasHISCOCode'],
            Literal(hiSheet.cell(i,1).value)
            ))
    graph.add((
            namespaces['cpo'][str(hiSheet.cell(i,1).value)],
            namespaces['rdfs']['label'],
            Literal(hiSheet.cell(i,0).value, lang='nl')
            ))

    # Local data structure
    hiCode = {}
    hiCode["code"] = str(hiSheet.cell(i,1).value)
    hiCode["label"] = hiSheet.cell(i,0).value
    hiCodes.append(hiCode)

# Serialize
fileWrite = open('hisco.ttl', "w")
turtle = graph.serialize(None, format='n3')
fileWrite.writelines(turtle)
fileWrite.close()


__author__ = "Albert Meronyo-Penyuela"
__copyright__ = "Copyright 2012, VU University Amsterdam"
__credits__ = ["Albert Meronyo-Penyuela"]
__license__ = "LGPL v3.0"
__version__ = "0.1"
__maintainer__ = "Albert Meronyo-Penyuela"
__email__ = "albert.merono@vu.nl"
__status__ = "Prototype"
