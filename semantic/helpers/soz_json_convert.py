from rdflib import BNode, Literal, URIRef, Graph, plugin, Namespace
from rdflib.plugins.parsers.notation3 import TurtleParser
from rdflib.namespace import RDF, FOAF, DC, DCTERMS, NamespaceManager, Namespace
import re
import json

thesoz_ns = Namespace("http://lod.gesis.org/thesoz/ext/")

g = Graph()
# ns_manager = NamespaceManager(g)
# ns_manager.bind('thesoz', thesoz_ns)
# ns_manager.bind('rdf', RDF)

skos_ttl = open('thesoz_0_93.ttl', 'r')
result = g.parse(skos_ttl, format='turtle')

#classes = g.triples([None, None, thesoz_ns.Classification])

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