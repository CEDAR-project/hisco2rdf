#!/usr/bin/env python

"""hisco2rdf.py: An RDF graph generator for the HISCO occupations system."""

import csv
from xlrd import open_workbook
from rdflib import ConjunctiveGraph, Namespace, Literal, RDF, RDFS

class hisco2rdf:
    """A HISCO to RDF converter"""

    def __init__(self, inputDataFile):
        """Load input data, initialize namespaces, initialize graph"""

        # Open workbook for input data
        self.hiscoSourceData = open_workbook(inputDataFile, formatting_info=True)
        self.hiscoSheet = self.hiscoSourceData.sheet_by_index(0)
        
        self.namespaces = {
            'cpo':Namespace('http://cedar-project.nl/harmonization/occupations/')
            }

        self.graph = ConjunctiveGraph()

    def buildGraph(self):
        """Populate the graph with relevant HISCO triples"""

        print "Building RDF graph for HISCO..."
        
        for namespace in self.namespaces:
            self.graph.namespace_manager.bind(namespace, self.namespaces[namespace])

        ## Cols to read: [0,1] Rows to read: [2:53216]
        for i in range(1,53216):
            self.graph.add((
                    self.namespaces['cpo'][str(self.hiscoSheet.cell(i,1).value)],
                    RDF.type,
                    self.namespaces['cpo']['HISCOOccupation']
                    ))
            self.graph.add((
                    self.namespaces['cpo'][str(self.hiscoSheet.cell(i,1).value)],
                    self.namespaces['cpo']['hasHISCOCode'],
                    Literal(self.hiscoSheet.cell(i,1).value)
                    ))
            self.graph.add((
                    self.namespaces['cpo'][str(self.hiscoSheet.cell(i,1).value)],
                    RDFS.label,
                    Literal(self.hiscoSheet.cell(i,0).value, lang='nl')
                    ))

    def serializeGraph(self, outputDataFile):
        """Serialize the generated graph to the specified output file"""

        print "Serializing graph to {}...".format(outputDataFile)

        self.fileToWrite = open(outputDataFile, "w")
        self.turtleFile = self.graph.serialize(None, format='n3')
        self.fileToWrite.writelines(self.turtleFile)
        self.fileToWrite.close()

if __name__ == "__main__":
    hiscoRDFGenerator = hisco2rdf('data/HISCO.xls')
    hiscoRDFGenerator.buildGraph()
    hiscoRDFGenerator.serializeGraph('hisco.ttl')


__author__ = "Albert Meronyo-Penyuela"
__copyright__ = "Copyright 2012, VU University Amsterdam"
__credits__ = ["Albert Meronyo-Penyuela"]
__license__ = "LGPL v3.0"
__version__ = "0.1"
__maintainer__ = "Albert Meronyo-Penyuela"
__email__ = "albert.merono@vu.nl"
__status__ = "Prototype"
