from StringIO import StringIO
from pybtex.database.input import bibtex
from string import strip
from caselessdict import CaselessDict
from xml.sax.saxutils import quoteattr

DUMMY='@article{DUMMY, Author = {No Boby}, Title = {This is a dummy entry.}}'

def getEntryFromString(s):
    parser = bibtex.Parser()
    try:
	bib = parser.parse_stream(StringIO(s))
	key,entry = bib.entries.items()[0]
    except:
	bib = parser.parse_stream(StringIO(DUMMY))
	key,entry = bib.entries.items()[0]
    return entry

TYPE2CATEGORY=CaselessDict({\
'article':'journal',
'book':'book',
'techreport':'report',
'misc':'private communication',
'inproceedings':'proceedings',
})

def BibTeX2XML(bibtexstring):
    e = getEntryFromString(bibtexstring)
    xml = u'<Source sourceID="B%s">\n<Authors>\n'%e.key
    for a in e.persons['author']:
        name = a.first() + a.middle() + a.last() + a.lineage()
        name = map(strip,name)
        name = map(strip,name,['{}']*len(name))
        xml += '<Author><Name>%s</Name></Author>'%' '.join(name)
    xml += '\n</Authors>'

    category = TYPE2CATEGORY.get(e.type)
    
    f = CaselessDict(e.fields)
    url = f.get('bdsk-url-1')
    title = f.get('title').strip().strip('{}')
    sourcename = f.get('journal','unknown')
    doi = f.get('doi')
    year = f.get('year')
    volume = f.get('volume')
    pages = f.get('pages')
    if pages: p1,p2 = pages.split('-')
    else: p1,p2 = '',''

    xml += """<Title>%s</Title>
<Category>%s</Category>
<Year>%s</Year>
<SourceName>%s</SourceName>
<Volume>%s</Volume>
<PageBegin>%s</PageBegin>
<PageEnd>%s</PageEnd>
<UniformResourceIdentifier>%s</UniformResourceIdentifier>
<DigitalObjectIdentifier>%s</DigitalObjectIdentifier>
""" % (title,category,year or 2222,sourcename,volume,p1,p2,url,doi)

    xml += '<BibTeX>%s</BibTeX></Source>'%quoteattr(bibtexstring)[1:-1]

    return xml
