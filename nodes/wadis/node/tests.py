import sys
from django.http import QueryDict, HttpRequest
from django.utils.importlib import import_module
from lxml import objectify, etree

from django.conf import settings
#Warning! Forced DEBUG = FALSE in DjangoTestSuiteRunner->setup_test_environment->settings.DEBUG = False
from models import *
from nodes.wadis.node import transforms
from nodes.wadis.node.queryfunc import getSources

INCHI = import_module(settings.UTILPKG + ".inchi")
DICTS = import_module(settings.NODEPKG + '.dictionaries')
if 'NodeID' in DICTS.RETURNABLES:
	NODEID = DICTS.RETURNABLES['NodeID']
else:
	NODEID = 'fake'

try:
	from django.utils.unittest import TestCase
except ImportError:
	from django.test import TestCase
try:
	from django.utils import unittest
except ImportError:
	import unittest

from django.test.client import Client
from vamdctap import views


from other.verification.test import LocalResolver
parser = etree.XMLParser()
xsdPath = settings.BASE_PATH + "/other/verification/xsd/xsams/0.3/xsams.xsd"
parser.resolvers.add(LocalResolver({"http://vamdc.org/xml/xsams/0.3/" : xsdPath}))
xsd=etree.XMLSchema(etree.parse(xsdPath, parser=parser))
#The libxml2 has a bug 170795 (reported: 2005). XML Schemas doesn't validate IDREF/IDREFS attributes.

testClient = Client()


def toDict(queryDict):
	dict = {}
	for key in queryDict:
		dict[key] = queryDict[key]
	return dict


class TapSyncTest(TestCase):
	prefixURL = "/tap/sync?"
	query = "LANG=VSS1&FORMAT=XSAMS&QUERY="


	def setUp(self):
		self.request = HttpRequest()
		self.request.META["REMOTE_ADDR"] = 'localhost'
		self.queryDict = toDict(QueryDict(self.query))


	def testGetSources(self):
		settings.DEBUG = True

		transitions = Transition.objects.select_related().filter(id_transition_ds=17)
		sources = getSources(transitions)
		if len(sources) == 1:
			self.assertEquals('2', sources[0].getArticleNumber())
			authors = [u'L.S. Rothman', u'D. Jacquemart', u'A. Barbe', u'D.C. Benner', u'M. Birk', u'L.R. Brown', u'M. Carleer', u'C.Chackerian Jr', u'K. Chance', u'L.H. Coudert', u'V. Dana', u'V.M. Devi', u'J.-M. Flaud', u'R.R. Gamache', u'A.Goldman', u'J.-M. Hartmann', u'K.W. Jucks', u'A.G. Maki', u'etc']
			self.assertEquals(authors, sources[0].getAuthorList())
			self.assertEquals('journal', sources[0].biblioTypeName)
			self.assertRegexpMatches(sources[0].biblioannotation, r" HITRAN ")
			self.assertEquals('10.1016/j.jqsrt.2004.10.008', sources[0].bibliodoi)
			self.assertEquals(931, sources[0].biblioid)
			self.assertEquals('Journal of Quantitative Spectroscopy and Radiation Transfer', sources[0].getSourceName())
			self.assertEquals('139', sources[0].getPageBegin())
			self.assertEquals('204', sources[0].getPageEnd())
			self.assertEquals('The HITRAN 2004 Molecular Spectroscopic Database', sources[0].biblioname)
			self.assertEquals(None, sources[0].bibliourl)
			self.assertEquals('96', sources[0].bibliovolume)
			self.assertEquals(2005, sources[0].biblioyear)
		else:
			self.fail("Sources is empty")


	def testSyncSelectMoleculeEnergy(self):
		settings.DEBUG = True
		sql = "SELECT All WHERE StateEnergy > 9895.327 AND StateEnergy < 9895.328"
		self.queryDict["QUERY"] = sql
		self.request.REQUEST = self.queryDict

		content = views.sync(self.request).content
		objTree = objectify.fromstring(content)
		actual = etree.tostring(objTree, pretty_print=True)
		xsd.assertValid(objTree)

		expected = etree.tostring(objectify.fromstring(open(settings.BASE_PATH + "/nodes/" + settings.NODENAME + "/test/Energy.xml").read()), pretty_print=True)
		self.assertEquals(expected, actual)


	def testSyncSelectMoleculeH_17OD_W_EC(self):
		settings.DEBUG = True
		sql = "SELECT All WHERE ((Inchi='InChI=1S/H2O/h1H2/i1+1/hD'  AND RadTransWavenumber > 1234.23 AND RadTransWavenumber < 1244.24) AND MethodCategory = 'experiment')"
		self.queryDict["QUERY"] = sql
		self.request.REQUEST = self.queryDict

		content = views.sync(self.request).content
		objTree = objectify.fromstring(content)
		actual = etree.tostring(objTree, pretty_print=True)
		xsd.assertValid(objTree)

		expected = etree.tostring(objectify.fromstring(open(settings.BASE_PATH + "/nodes/" + settings.NODENAME + "/test/H_17OD_W_EC.xml").read()), pretty_print=True)
		self.assertEquals(expected, actual)


	def testSyncSelectMoleculeInchiKey(self):
		settings.DEBUG = True
		sql = "SELECT All WHERE (InchiKey='RWSOTUBLDIXVET-IQRQJSDFSA-N'  AND RadTransWavenumber > 40 AND RadTransWavenumber < 45) OR (Inchi IN ('InChI=1S/H2O/h1H2') AND RadTransWavenumber > 1239.2185 AND RadTransWavenumber < 1239.2191)"
		self.queryDict["QUERY"] = sql
		self.request.REQUEST = self.queryDict

		objTree = objectify.fromstring(views.sync(self.request).content)
		actual = etree.tostring(objTree, pretty_print=True)
		xsd.assertValid(objTree)

		expected = etree.tostring(objectify.fromstring(open(settings.BASE_PATH + "/nodes/" + settings.NODENAME + "/test/InchiKey.xml").read()), pretty_print=True)
		self.assertEquals(expected, actual)


	def testSelectMoleculeInchiKey(self):
		sql = "SELECT+All+WHERE+InchiKey='RWSOTUBLDIXVET-IQRQJSDFSA-N'"
		objTree = objectify.fromstring(testClient.get(self.prefixURL + self.query + sql.strip()).content)
		xsd.assertValid(objTree)


	def testSelectRadTransWavenumber(self):
		sql = "SELECT+All+WHERE+RadTransWavenumber+>+1239+AND+RadTransWavenumber+<+1240"
		objTree = objectify.fromstring(testClient.get(self.prefixURL + self.query + sql.strip()).content)
		xsd.assertValid(objTree)


	def tearDown(self):
		pass



class TransformsTestCase(TestCase):
	def setUp(self):
		pass


	def testInchi2Id(self):
		self.assertEquals(['inner.id_substance', 'in', '(', '1000021', ')'], transforms.inchi2Id('Inchi', 'in', '(', "'InChI=1S/H2O/h1H2'", ')'))

	def testInchiKey2Id(self):
		self.assertEquals(['inner.id_substance', 'in', '(', '1000021', ')'], transforms.inchiKey2Id('Inchi', 'in', '(', "'XLYOFNOQVPJJNP-UHFFFAOYSA-N'", ')'))

	def testMethodCategory2Type(self):
		self.assertEquals(['inner.type', '=', '0'], transforms.methodCategory2Type('MethodCategory', '=', '"theory"'))

	def tearDown(self):
		pass



class SagaModelTestCase(TestCase):
	def setUp(self):
		pass


	def testGetCharge(self):
		self.assertEquals("+1", Substancecorr.objects.get(id_substance=1000529).getCharge())

	def testGetLatexFormula(self):
		substance = Substancecorr.objects.get(id_substance=1000529)
		self.assertEquals("$NO^+$", substance.getLatexFormula())

		substance.plain_name = "_17H12_2O_1plus_1Fe_2minus_2S2I_plus"
		self.assertEquals("$^{17}H_{12}^2O^+Fe^{2-}^2S_2I^+$", substance.getLatexFormula())

	def testGetABCFormula(self):
		substance = Substancecorr.objects.get(id_substance=1000388)
		self.assertEquals("CH2O2", substance.getABCFormula())

		substance.plain_name = "_17H12_2O_1T2_1Fe_2Ti3_2S2F_2plus"
		self.assertEquals("FFeH14OS2Ti3+2", substance.getABCFormula())

	def testGetSubstances(self):
		self.assertEquals("XLYOFNOQVPJJNP-UHFFFAOYSA-N", SubstanceDict.byInchi["InChI=1S/H2O/h1H2"].id_inchi_key)


	def tearDown(self):
		pass



class InchiTestCase(TestCase):
	def setUp(self):
		pass


	def testInchiToInciKey(self):
		self.assertEquals("XLYOFNOQVPJJNP-UHFFFAOYSA-N", INCHI.inchiToInchiKey("InChI=1S/H2O/h1H2"))


	def tearDown(self):
		pass



def suite():
	tsuite = unittest.TestSuite()

	tsuite.addTest(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))

	#from vamdctap import tests as vamdctests
	#tsuite.addTest(unittest.defaultTestLoader.loadTestsFromModule(vamdctests))

	return tsuite

