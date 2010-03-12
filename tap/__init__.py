"""
Tools to query the TAP-interface of DSA/catalog.
It's a asynchronous request and the replies are XML
documents (that can be tranformed into html).

The scripts sends a (hardcoded) request to my
DSA/catalog installation with VALD data. It then
tells DSA to run the query, checks if it has completed
and fetches the result.

Not yet working: read the result into ATPy's implementation
of VOTable.

"""

# don't use a proxy
from os import environ
environ["http_proxy"]=''

import urllib
from lxml import etree as e
from lxml.etree import XPath

from time import sleep
import atpy
from StringIO import StringIO
import threading


from tapclass import *
