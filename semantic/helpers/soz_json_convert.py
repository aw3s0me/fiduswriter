from rdflib import BNode, Literal, URIRef, Graph, plugin, Namespace
from rdflib.plugins.parsers.notation3 import TurtleParser
from rdflib.namespace import RDF, FOAF, DC, DCTERMS, NamespaceManager, Namespace
import re
import json
import urllib
import zipfile

thesoz_ns = Namespace("http://lod.gesis.org/thesoz/ext/")

def download_thesoz():
    thesoz_addr = 'http://www.etracker.de/lnkcnt.php?et=qPKGYV&url=http://www.gesis.org/fileadmin/upload/dienstleistung/tools_standards/thesoz_skos_turtle.zip&lnkname=fileadmin/upload/dienstleistung/tools_standards/thesoz_skos_turtle.zip'
    zip_file_name = 'thesoz_0_93.zip'

    urllib.urlretrieve(thesoz_addr, zip_file_name)

    fh = open(zip_file_name, 'rb')
    z = zipfile.ZipFile(fh)
    z.extractall()
    fh.close()

download_thesoz()

g = Graph()

skos_ttl = open('thesoz_0_93.ttl', 'r')
result = g.parse(skos_ttl, format='turtle')

query = """
        PREFIX thesoz: <http://lod.gesis.org/thesoz/ext/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        select distinct ?class ?name
            where {
                ?class a thesoz:Classification.
                ?class skos:prefLabel ?name.
                FILTER(langMatches(lang(?name), "EN"))
            }
        """
query_res = g.query(query)
regex_query = re.compile(ur'([0-9][0-9.]*[0-9]*)', re.UNICODE)

final_json = dict()

for row in query_res:
    res = re.search(regex_query, row[0])
    class_code = res.group(0)
    final_json[class_code] = row[1].value

skos_ttl.close()

with open('soz_lookup.json', 'w') as fp:
    json.dump(final_json, fp)