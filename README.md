hisco2rdf
=========

Script that generates an RDF graph for the History of Work Information System

**Author**: [Albert Meroño-Peñuela](http://github.com/albertmeronyo)

**Copyright**: VU University Amsterdam

**License**: [LGPL v3.0](http://www.gnu.org/licenses/lgpl.html)

## What is this?

[HISCO](http://historyofwork.iisg.nl/), the History of Work Information System, is a classification of tens of thousands of historical occupations from all around the world between the 16th and the 20th century. It provides a coding system (i.e. unique identifiers) that classify job labels written in different languages, improving interoperability between systems storing data about historical occupations (e.g. censuses).

Although a digital version is available, no RDF version of this dataset currently exists. An RDF version of HISCO would be of great value for interlinking historical datasets in the Web of Linked Data.

## How does it work?

Invoke `python hisco2rdf.py` from the command line. A `hisco.ttl` file with the HISCO RDF graph will be produced.

Currently only the provided HISCO source data file is supported (`data/HISCO.xls`).

## Data model

URIs are generated for each HISCO occupation entry (i.e. unique identifier). All related labels are conveniently linked.

<img src='http://github.com/CEDAR-project/hisco2rdf/raw/master/img/hisco-datamodel.png'/>

## Requirements

* Python 2.7
* xlrd package <http://www.python-excel.org>
* RDFLib package <http://www.rdflib.net>