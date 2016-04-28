from rdflib import BNode, Literal, URIRef, Graph, plugin, Namespace
from rdflib.plugins.parsers.notation3 import TurtleParser
from rdflib.namespace import RDF, FOAF, DC, DCTERMS, NamespaceManager, Namespace
import re
import json
import urllib
import zipfile
import os

thesoz_ns = Namespace("http://lod.gesis.org/thesoz/ext/")
thesoz_ttl_location = '../static/ttl/'

def download_thesoz():
    thesoz_addr = 'http://www.etracker.de/lnkcnt.php?et=qPKGYV&url=http://www.gesis.org/fileadmin/upload/dienstleistung/tools_standards/thesoz_skos_turtle.zip&lnkname=fileadmin/upload/dienstleistung/tools_standards/thesoz_skos_turtle.zip'
    zip_file_name = 'thesoz_0_93.zip'

    urllib.urlretrieve(thesoz_addr, zip_file_name)

    fh = open(zip_file_name, 'rb')
    z = zipfile.ZipFile(fh)
    z.extract('thesoz_0_93.ttl', thesoz_ttl_location)
    fh.close()

    os.remove(zip_file_name)

def remove_illegal(ttl):
    regex_remove_illegal_str = re.compile(ur'(skos:prefLabel|dc:creator|cc:attributionName|skos:definition|dc:publisher|de\s+,{1})\s{1}".*(\n{1}).*"@', re.UNICODE)
    result = re.sub(regex_remove_illegal_str, lambda m: m.group(0).replace('\n',' '), ttl)

    return result

download_thesoz()

g = Graph()

skos_ttl = open(thesoz_ttl_location + 'thesoz_0_93.ttl', 'r')
ttl_str = skos_ttl.read()
ttl_str = remove_illegal(ttl_str)

result = g.parse(data=ttl_str, format='turtle')

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

with open('../static/json/soz_lookup.json', 'w') as fp:
    json.dump(final_json, fp)
