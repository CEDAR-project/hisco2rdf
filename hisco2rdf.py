#!/usr/bin/env python

"""hisco2rdf.py: An RDF graph generator for the HISCO occupations system."""

import csv
from xlrd import open_workbook
from rdflib import ConjunctiveGraph, Namespace, Literal, RDF, RDFS, URIRef
from HTMLParser import HTMLParser
import urllib2

class HISCOFirstLevelParser(HTMLParser):
    # Flags
    tableFlag = False
    spanFlag = False
    aFlag = False

    def handle_starttag(self, tag, attrs):
        if tag == 'span' and ('class', 'nextprevbutton') in attrs:
            self.spanFlag = True
        if tag == 'table':
            self.tableFlag = True
        if tag == 'a':
            self.aFlag = True
    def handle_endtag(self, tag):
        if tag == 'table':
            self.tableTag = False
        if tag == 'a':
            self.aFlag = False
            self.spanFlag = False
    def handle_data(self, data):
        # HISCO class name
        if self.tableFlag and self.spanFlag and self.aFlag:
            print data

class HISCOParser(HTMLParser):
    def __init__(self, g, n):
        HTMLParser.__init__(self)        
        self.spanFlag = False
        self.recordFlag = False
        self.aFlag = False
        self.tdFlag = False
        self.graph = g
        self.namespaces = n
        self.lastURI = ''
    def handle_starttag(self, tag, attrs):
        if ('class', 'rubri_code') in attrs:
            self.spanFlag = True
            self.recordFlag = True
        if tag == 'a':
            self.aFlag = True
        if tag == 'td':
            self.tdFlag = True
    def handle_endtag(self, tag):
        if tag == 'span' or tag == 'p':
            self.spanFlag = False
        if tag == 'tr':
            self.recordFlag = False
        if tag == 'a':
            self.aFlag = False
        if tag == 'td':
            self.tdFlag = False
    def handle_data(self, data):
        # HISCO class name
        if self.recordFlag and self.spanFlag and not data.strip() == '':
            self.lastURI = data
            if len(self.lastURI) == 5:
                self.boraderURI = self.lastURI[:-2]
            else:
                self.broaderURI = self.lastURI[:-1]
            self.graph.add((URIRef('http://historyofwork.iisg.nl/resource/' + str(self.lastURI)),
                            RDF.type,
                            self.namespaces['skos'].Concept))
            self.graph.add((URIRef('http://historyofwork.iisg.nl/resource/' + str(self.lastURI)),
                            self.namespaces['skos']['broader'],
                            URIRef('http://historyofwork.iisg.nl/resource/' + str(self.broaderURI))))
        if self.recordFlag and self.aFlag and not data.strip() == '' and not data == 'Display Titles':
            self.graph.add((URIRef('http://historyofwork.iisg.nl/resource/' + str(self.lastURI)),
                            self.namespaces['skos']['prefLabel'],
                            Literal(data, 'en')))
        if self.recordFlag and not self.aFlag and not self.spanFlag and self.tdFlag and not data.strip() == '':
            self.graph.add((URIRef('http://historyofwork.iisg.nl/resource/' + str(self.lastURI)),
                            self.namespaces['skos']['definition'],
                            Literal(data, 'en')))

class hisco2rdf:
    """A HISCO to RDF converter"""

    def __init__(self):
        """Load data, initialize namespaces, initialize graph"""

        self.graph = ConjunctiveGraph()

        self.hiscoSource = "http://historyofwork.iisg.nl/major.php"
        self.totalMinors = 10
        self.totalRubrisFirst = 10
        self.totalRubrisSecond = 100
        self.totalMicros = 100
        self.startDetailMicro = 35038
        self.endDetailMicro = 36711
        self.firstLevelParser = HISCOFirstLevelParser()
        
        self.namespaces = {
            'cpo':Namespace('http://cedar-project.nl/harmonization/occupations/'),
            'skos':Namespace('http://www.w3.org/2004/02/skos/core#')
            }

        self.parser = HISCOParser(self.graph, self.namespaces)

        self.parseTree()

    def parseTree(self):
        """Parse the HISCO tree from IISG website"""

        for namespace in self.namespaces:
            self.graph.namespace_manager.bind(namespace, self.namespaces[namespace])

        # Parse major nodes
        opener = urllib2.build_opener()
        try:
            infile = opener.open(self.hiscoSource)
            self.firstLevelParser.feed(infile.read())
        except:
            pass

        # Parse minor nodes
        for i in range(self.totalMinors):
            opener = urllib2.build_opener()
            try:
                infile = opener.open('http://historyofwork.iisg.nl/list_minor.php?text01=' + str(i) + '&&text01_qt=strict')
                self.parser.feed(infile.read())
            except:
                pass

        # Parse rubri nodes, first level
        for i in range(1, self.totalRubrisFirst):
            opener = urllib2.build_opener()
            try:
                infile = opener.open('http://historyofwork.iisg.nl/list_rubri.php?keywords=0' + str(i) + '&keywords_qt=lstrict&orderby=keywords')
                self.parser.feed(infile.read())
            except:
                pass

        # Parse rubri nodes, second level
        for i in range(11, self.totalRubrisSecond):
            opener = urllib2.build_opener()
            try:
                infile = opener.open('http://historyofwork.iisg.nl/list_rubri.php?keywords=0' + str(i) + '&keywords_qt=lstrict&orderby=keywords')
                self.parser.feed(infile.read())
            except:
                pass

        # Parse micro nodes
        for i in range(11, self.totalMicros):
            opener = urllib2.build_opener()
            try:
                infile = opener.open('http://historyofwork.iisg.nl/list_micro.php?keywords=0' + str(i)  + '&keywords_qt=lstrict')
                self.parser.feed(infile.read())
            except:
                pass

        # Parse leaves (detail micros)
        for i in range(self.startDetailMicro, self.endDetailMicro + 1):
            opener = urllib2.build_opener()
            try:
                infile = opener.open('http://historyofwork.iisg.nl/detail_micro.php?know_id=' + str(i) + '&lang=')
                self.parser.feed(infile.read())
            except:
                pass
            
    def serializeGraph(self, outputDataFile):
        """Serialize the generated graph to the specified output file"""

        print "Serializing graph to {}...".format(outputDataFile)

        self.fileToWrite = open(outputDataFile, "w")
        self.turtleFile = self.graph.serialize(None, format='n3')
        self.fileToWrite.writelines(self.turtleFile)
        self.fileToWrite.close()

if __name__ == "__main__":
    hiscoRDFGenerator = hisco2rdf()
    hiscoRDFGenerator.serializeGraph('hisco.ttl')


__author__ = "Albert Meronyo-Penyuela"
__copyright__ = "Copyright 2013, VU University Amsterdam"
__credits__ = ["Albert Meronyo-Penyuela"]
__license__ = "LGPL v3.0"
__version__ = "0.2"
__maintainer__ = "Albert Meronyo-Penyuela"
__email__ = "albert.merono@vu.nl"
__status__ = "Prototype"
