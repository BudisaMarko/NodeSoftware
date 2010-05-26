# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# import your models 
#from DjVALD.vald.models import Transition,State,Source,Species

# This imports all the generic tap views!
from DjNode.tapservice.views import *

# The generators
from DjNode.tapservice.generators import *

# An example of a replacement dictionary
#VALD_DICT={'1':'species__atomic',
#           '2':'species__ion',
#           '3':'vacwave',
#           '4':'airwave',
#           '5':'loggf',
#           '6':'lostate__energy',
#           '7':'lostate__J',
#           }


def index(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)




### VALD-specific helper functions, as an example


def getVALDsources(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return Source.objects.filter(pk__in=sids)

def getVALDstates(transs):
    #lostates=State.objects.filter(islowerstate_trans__in=transs)
    #histates=State.objects.filter(islowerstate_trans__in=transs)
    #states = lostates | histates
    q1,q2=Q(islowerstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    return State.objects.filter(q1|q2).distinct()
    



def setupResults(tap,limit=0):
    if tap.lang=='vamdc':
        tap.query=tap.query%VALD_DICT
        print tap.query
        #transs = Transition.objects.extra(tables=['species','states'],where=[tap.query,'(transitions.lostate=states.id OR transitions.upstate=states.id)','transitions.species=species.id'],).order_by('airwave')
        qtup=vamdc2queryset(tap.query)
        transs = Transition.objects.filter(*qtup).order_by('airwave')
    else:
        qtup=parseSQL(tap.query)
        transs = Transition.objects.filter(*qtup).order_by('airwave')
    
    totalcount=transs.count()
    if limit :
        transs = transs[:limit]

    sources = getVALDsources(transs)
    states = getVALDstates(transs)
    if limit:
        return transs,states,sources,totalcount
    else:
        return transs,states,sources
