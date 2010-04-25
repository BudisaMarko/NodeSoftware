# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.forms.formsets import formset_factory

from DjVAMDC.portal.models import Query

import string as s
from random import choice
def makeQID(length=6, chars=s.letters + s.digits):
    return ''.join([choice(chars) for i in xrange(length)])

VALD_DICT={'1':'species.atomic',
           '2':'species.ion',
           '3':'transitions.vacwave',
           '4':'transitions.airwave',
           '5':'transitions.loggf',
           '6':'state.energy',
           '7':'state.J',
           }

REGISTRY=[
          {'name':'VALD','url':'http://vamdc.fysast.uu.se:8888/node/vald/sync/','coldict':VALD_DICT},
          {'name':'VALD2','url':'http://vamdc.fysast.uu.se:8888/node/vald/sync/','coldict':VALD_DICT},
          ]


PARA_CHOICES=[(0,u''),
              (1,u'Atomic number'),
              (2,u'Ionization'),
              (3,u'Wavelength in vaccum (Å)'),
              (4,u'Wavelength in air (Å)'),
              (5,u'log(g*f)'),
              (6,u'Level energy (1/cm)'),
              (7,u'Total angular momentum J'),
              (8,u'Species from species list (not implemented)'),
]

class ConditionForm(forms.Form):
    lower=forms.DecimalField(max_digits=6,required=False,initial=None,label='lower bound',widget=forms.widgets.TextInput(attrs={'size':'8'}))
    parameter=forms.ChoiceField(label='parameter to restrict',required=True,initial='',choices=PARA_CHOICES)
    upper=forms.DecimalField(max_digits=6,required=False,initial=None,label='upper bound',widget=forms.widgets.TextInput(attrs={'size':'8'}))
    connection=forms.BooleanField(initial=True,required=False,label='Use AND to connect with next condition?')
    
    def validate(self,value):
        # check here e.g. if the lower bound <= upper
        super(ConditionForm,self).validate(value)              

def constructQuery(constraints):
    q='SELECT ALL WHERE '
    for c in constraints:
        if c['parameter']=='0': continue
        if c['lower'] and c['upper']:
            if c['lower'] == c['upper']: q+='( %%(%s) = %s )'%(c['parameter'],c['upper'])
            else:
                q+='( %%(%s) > %s AND '%(c['parameter'],c['lower'])
                q+='%%(%s) < %s )'%(c['parameter'],c['upper'])
        elif c['lower']:
            q+='( %%(%s) > %s )'%(c['parameter'],c['lower'])
        elif c['upper']:
            q+='( %%(%s) < %s )'%(c['parameter'],c['upper'])
        else:
            q+='( %%(%s) notnull )'%c['parameter']

        if c['connection']: q+=' AND '
        else: q+=' OR '
    return q

def query(request):
    ConditionSet = formset_factory(ConditionForm, extra=5)
    if request.method == 'POST':
        selectionset = ConditionSet(request.POST,request.FILES) 
        if selectionset.is_valid():
            query=Query(qid=makeQID(),query=constructQuery(selectionset.cleaned_data))
            query.save()
            return HttpResponseRedirect('/portal/results/%s/'%query.qid) 
    else:
        selectionset = ConditionSet(initial=[
                {'lower': u'3000',
                 'upper': u'3500',
                 'parameter':4,
                 'connection':True,
                 },
                {'lower': u'26',
                 'upper': u'26',
                 'parameter':2,
                 'connection':True,
                 },
                ])
        
    return render_to_response('portal/query.html', {'selectionset': selectionset})


#####################

def askNode(node,query):
    pass

def results(request,qid):
    query=Query.objects.get(pk=qid)
    results=[]
    for node in REGISTRY:
        results.append(askNode(node,query))
        
    return render_to_response('portal/results.html', {'result': results, 'query':query})

###################

def index(request):
    c=RequestContext(request,{})
    return render_to_response('portal/index.html', c)

######################

class SQLqueryForm(forms.Form):
    sql=forms.CharField(label='Enter your SQL query',widget=forms.widgets.Textarea(attrs={'cols':'40','rows':'5'}),required=True)


def sqlquery(request):
    if request.method == 'POST':
        form = SQLqueryForm(request.POST) 
        if form.is_valid():
            print form.cleaned_data

    else:
        form=SQLqueryForm()
        
    return render_to_response('portal/sqlquery.html', {'form': form})

