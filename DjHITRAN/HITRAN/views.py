# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.db.models import Q

# import your models 
from DjHITRAN.HITRAN.models import *

### IMPORTANT NOTE This file must implement a function called 
### setupResults() which takes the parsed SQL from the query parser. 
### setupResults() must pass the restrictions on to one or several of 
### your models (depending on the database strcture) and also fetch the 
### corresponding items from other models that are needed in the return 
### data. setupResults() must return a DICTIONARY that has as keys some 
### of the following: Sources AtomStates MoleStates CollTrans RadTrans 
### Methods; with the corresponding QuerySets as the values for these 
### keys. This dictionary will be handed into the generator an allow it 
### to fill the XML schema.
###
### Below is an example, inspired by VALD that has a data model like 
### this:
### One for the Sources/References
### One for the Species
### One for the States (points to Species once, and to several 
###   references)
### One for Transitions (points twice to States (upper, lower) and to 
###   several Sources)
###
### In this layout, all restrictions in the query can be passed to
### the Transitions model (using the pointers between models to
### restrict eg. Transition.species.ionization) which facilitates
### things.
###
### Now we can code two helper functions that get the corresponding
### Sources and States to a selection of Transitions:

# a straight forward example of getting the unique list of
# states that correspond to a given list of transitions by
# use of the inverse foreign key.

import sys
def LOG(s):
    print >> sys.stderr, s

def getVALDstates(transs):
    q1,q2=Q(islowerstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    return State.objects.filter(q1|q2).distinct()
    
# For the Sources we use a python set to collect reference ids
# (which are not stored as foreignkeys in the model). This is faster
# because there are so many Sources which are the same and by getting
# rid of duplicates before asking the DB, we sve time.
def getVALDsources(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return Source.objects.filter(pk__in=sids)



# In order to map the global keywords that come in the query
# to the place in the data model where the corresponding data sits, we 
# use two dictionaries, called RESTRICTABLES and RETURNABLES.


RETURNABLES={\
'MolecularSpeciesChemicalName':'RadTran.molec_name',
'RadTransWavenumberExperimentalValue':'RadTran.nu',
'RadTransProbabilityTransitionProbabilityAValue':'RadTran.a',
}

RESTRICTABLES = {\
'MolecularSpeciesChemicalName':'molec_name',
'RadTransWavenumberExperimentalValue':'nu',
'RadTransProbabilityTransitionProbabilityAValue':'a',
}

# import a helper unction that converts the WHERE part of the query into 
# strings that define Q-objects when evaluated which in turn can be 
# passed to a model.
from DjNode.tapservice.sqlparse import *

# work out which molecules are present in the database:
loaded_molecules = Trans.objects.values('molec_name').distinct()
# and get their names and html-names from the molecules table:
molec_names = Molecules.objects.filter(molec_name__in=loaded_molecules).values('molec_name','molec_name_html')

def search_form(request):
	return render_to_response('search_form.html', {'molec_names': molec_names})

def search(request):
	numin = request.POST.get('numin')
	if numin: numin=float(numin)
	numax = request.POST.get('numax')
	if numax: numax=float(numax)
	Smin = request.POST.get('Smin')
	if Smin: Smin=float(Smin)

	selected_molecules=[]
	for molec_name in molec_names:
		if request.POST.get(molec_name['molec_name']):
			selected_molecules.append(molec_name['molec_name'])

	q = Trans.objects.all()
	if numin: q = q.filter(nu__gte=numin)
	if numax: q = q.filter(nu__lte=numax)
	if Smin: q = q.filter(s__gte=Smin)
	q = q.filter(molec_name__in=selected_molecules)

	return render_to_response('search_results.html', {'transitions': q, 'selected_molecules': selected_molecules})

def setupResults(sql):
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except Exception,e: LOG(e); return {}
    #q = 'molec_name="CO"'

    transs = Trans.objects.filter(q) 
    # use the functions from above  
    #sources = getVALDsources(transs)
    #states = getVALDstates(transs)
    LOG('Count: %s'%transs.count())

    # return the dictionary as described above
    return {\
        'RadTrans':transs,
	#'Sources':sources,
	#'AtomStates':states,
    }
