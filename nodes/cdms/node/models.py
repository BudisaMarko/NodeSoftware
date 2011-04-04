# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from django.db.models import *
#from vamdctap.bibtextools import *

class StatesMolecules( Model):
    resource =  CharField(max_length=12, db_column='Resource') # Field name made lowercase.
    stateid =  IntegerField(primary_key=True, db_column='StateID') # Field name made lowercase.
    speciesid =  IntegerField(db_column='E_ID')
    moleculeid =  IntegerField(db_column='MoleculeID') # Field name made lowercase.
    chemicalname =  CharField(max_length=600, db_column='ChemicalName', blank=True) # Field name made lowercase.
    molecularchemicalspecies =  CharField(max_length=600, db_column='MolecularChemicalSpecies') # Field name made lowercase.
    isotopomer =  CharField(max_length=300, db_column='Isotopomer', blank=True) # Field name made lowercase.
    stateenergyvalue =  FloatField(null=True, db_column='StateEnergyValue', blank=True) # Field name made lowercase.
    stateenergyunit =  CharField(max_length=12, db_column='StateEnergyUnit') # Field name made lowercase.
    stateenergyaccuracy =  FloatField(null=True, db_column='StateEnergyAccuracy', blank=True) # Field name made lowercase.
    mixingcoefficient =  FloatField(null=True, db_column='MixingCoefficient', blank=True) # Field name made lowercase.
    statenuclearstatisticalweight =  IntegerField(null=True, db_column='StateNuclearStatisticalWeight', blank=True) # Field name made lowercase.
    qn_rotstate =  CharField(max_length=1500, db_column='QN_RotState', blank=True) # Field name made lowercase.
    qn_vibstate =  CharField(max_length=1500, db_column='QN_VibState', blank=True) # Field name made lowercase.
    qn_elecstate =  CharField(max_length=300, db_column='QN_ElecState', blank=True) # Field name made lowercase.
    qn_string =  CharField(max_length=1500, db_column='QN_String', blank=True) # Field name made lowercase.
    egy_qn_tag =  IntegerField(null=True, db_column='EGY_QN_Tag', blank=True) # Field name made lowercase.
    egy_qn1 =  IntegerField(null=True, db_column='EGY_QN1', blank=True) # Field name made lowercase.
    egy_qn2 =  IntegerField(null=True, db_column='EGY_QN2', blank=True) # Field name made lowercase.
    egy_qn3 =  IntegerField(null=True, db_column='EGY_QN3', blank=True) # Field name made lowercase.
    egy_qn4 =  IntegerField(null=True, db_column='EGY_QN4', blank=True) # Field name made lowercase.
    egy_qn5 =  IntegerField(null=True, db_column='EGY_QN5', blank=True) # Field name made lowercase.
    egy_qn6 =  IntegerField(null=True, db_column='EGY_QN6', blank=True) # Field name made lowercase.
    e_id =  IntegerField(db_column='E_ID') # Field name made lowercase.
    egy_dat_id =  IntegerField(null=True, db_column='EGY_DAT_ID', blank=True) # Field name made lowercase.
    e_tag =  IntegerField(db_column='E_Tag') # Field name made lowercase.
    class Meta:
        db_table = u'StatesMolecules'
    


class Molecules( Model):
     speciesid   =  IntegerField(primary_key=True, db_column='I_ID')
     inchi       =  CharField(max_length=200, db_column='I_Inchi', blank=True)
     inchikey    =  CharField(max_length=100, db_column='I_Inchikey', blank=True)
     name        =  CharField(max_length=100, db_column='I_Name', blank=True)
     htmlname    =  CharField(max_length=200, db_column='I_HtmlName', blank=True)
     latexname   =  CharField(max_length=100, db_column='I_LatexName', blank=True)
     stoichiometricformula =  CharField(max_length=200, db_column='I_StoichiometricFormula', blank=True)
     trivialname =  CharField(max_length=200, db_column='I_TrivialName', blank=True)
     class Meta:
         db_table = u'Isotopologs'

     statesspecies = ForeignKey(StatesMolecules, related_name='molecules',
                            db_column='I_ID')

class RadiativeTransitions(Model):

    resource =  CharField(max_length=12, db_column='Resource') # Field name made lowercase.
    radiativetransitionid =  IntegerField(primary_key=True, db_column='RadiativeTransitionID') # Field name made lowercase.
    moleculeid =  IntegerField(db_column='MoleculeID') # Field name made lowercase.
    speciesid =  IntegerField(db_column='E_ID')
    species = ForeignKey(Molecules, related_name='isspecies', db_column='E_ID', null=False)
    chemicalname =  CharField(max_length=600, db_column='ChemicalName', blank=True) # Field name made lowercase.
    molecularchemicalspecies =  CharField(max_length=600, db_column='MolecularChemicalSpecies') # Field name made lowercase.
    isotopomer =  CharField(max_length=300, db_column='Isotopomer', blank=True) # Field name made lowercase.
    energywavelength =  CharField(max_length=27, db_column='EnergyWavelength') # Field name made lowercase.
    wavelengthwavenumber =  CharField(max_length=33, db_column='WavelengthWavenumber') # Field name made lowercase.
    frequencyvalue =  FloatField(null=True, db_column='FrequencyValue', blank=True) # Field name made lowercase.
    frequencyunit =  CharField(max_length=9, db_column='FrequencyUnit') # Field name made lowercase.
    energywavelengthaccuracy =  FloatField(null=True, db_column='EnergyWavelengthAccuracy', blank=True) # Field name made lowercase.
    wavelengthvalue =  FloatField(null=True, db_column='WavelengthValue', blank=True) # Wavelength 
    wavelengthunit =  CharField(max_length=15, db_column='WavelengthUnit')
    multipole =  CharField(max_length=6, db_column='Multipole') # Field name made lowercase.
    log10weightedoscillatorstrengthvalue =  FloatField(null=True, db_column='Log10WeightedOscillatorStrengthValue', blank=True) # Field name made lowercase.
    log10weightedoscillatorstrengthunit =  CharField(max_length=24, db_column='Log10WeightedOscillatorStrengthUnit') # Field name made lowercase.
    einsteinA =  FloatField(null=True, db_column='EinsteinA', blank=True)
    lowerstateenergyvalue =  FloatField(null=True, db_column='LowerStateEnergyValue', blank=True) # Field name made lowercase.
    lowerstateenergyunit =  CharField(max_length=12, db_column='LowerStateEnergyUnit') # Field name made lowercase.
    upperstatenuclearstatisticalweight =  IntegerField(null=True, db_column='UpperStateNuclearStatisticalWeight', blank=True) # Field name made lowercase.
#    initialstateref =  IntegerField(null=True, db_column='InitialStateRef', blank=True) # Field name made lowercase.
#    finalstateref =  IntegerField(null=True, db_column='FinalStateRef', blank=True) # Field name made lowercase.
    initialstateref =  ForeignKey(StatesMolecules, related_name='isinitialstate',
                                db_column='InitialStateRef', null=False)

    finalstateref   =  ForeignKey(StatesMolecules, related_name='isfinalstate',
                                db_column='FinalStateRef', null=False)


    caseqn =  IntegerField(null=True, db_column='CaseQN', blank=True) # Field name made lowercase.
    qn_up_1 =  IntegerField(null=True, db_column='QN_Up_1', blank=True) # Field name made lowercase.
    qn_up_2 =  IntegerField(null=True, db_column='QN_Up_2', blank=True) # Field name made lowercase.
    qn_up_3 =  IntegerField(null=True, db_column='QN_Up_3', blank=True) # Field name made lowercase.
    qn_up_4 =  IntegerField(null=True, db_column='QN_Up_4', blank=True) # Field name made lowercase.
    qn_up_5 =  IntegerField(null=True, db_column='QN_Up_5', blank=True) # Field name made lowercase.
    qn_up_6 =  IntegerField(null=True, db_column='QN_Up_6', blank=True) # Field name made lowercase.
    qn_low_1 =  IntegerField(null=True, db_column='QN_Low_1', blank=True) # Field name made lowercase.
    qn_low_2 =  IntegerField(null=True, db_column='QN_Low_2', blank=True) # Field name made lowercase.
    qn_low_3 =  IntegerField(null=True, db_column='QN_Low_3', blank=True) # Field name made lowercase.
    qn_low_4 =  IntegerField(null=True, db_column='QN_Low_4', blank=True) # Field name made lowercase.
    qn_low_5 =  IntegerField(null=True, db_column='QN_Low_5', blank=True) # Field name made lowercase.
    qn_low_6 =  IntegerField(null=True, db_column='QN_Low_6', blank=True) # Field name made lowercase.
    e_id =  IntegerField(db_column='E_ID') # Field name made lowercase.
    e_tag =  IntegerField(db_column='E_Tag') # Field name made lowercase.
    e_states =  CharField(max_length=600, db_column='E_States', blank=True) # Field name made lowercase.
    e_name =  CharField(max_length=600, db_column='E_Name') # Field name made lowercase.
#    def getRefs(self,which):
#        try:
#            id = eval('self.'+which+'_ref_id')
#            return refcache[id]
#        except:
#            return None

    def __unicode__(self):
        return u'ID:%s Freq: %s'%(self.radiativetransitionid,self.frequencyvalue)
    class Meta:
        db_table = u'RadiativeTransitions'




class MolecularQuantumNumbers( Model): 

    stateid =  IntegerField(primary_key=True, db_column='StateID')
    case =  CharField(max_length=10, db_column='Case')
    label =  CharField(max_length=50, db_column='Label')
    value =  CharField(max_length=100, db_column='Value')
    spinref =  CharField(max_length=100, db_column='SpinRef')
    attribute =  CharField(max_length=100, db_column='Attribute')

    class Meta:
        db_table = 'MolQN'

    statesmolecules =  ForeignKey(StatesMolecules, related_name='quantumnumbers', 
                            db_column='StateID')



class SourcesIDRefs( Model):
    rlId  =  IntegerField(primary_key=True, db_column='RL_ID')
    rId   =  IntegerField(null=True, db_column='RL_R_ID')
    eId   =  IntegerField(null=True, db_column='RL_E_ID')
    datId =  IntegerField(null=True, db_column='RL_DAT_ID', blank=True)
    fId   =  IntegerField(null=True, db_column='RL_F_ID', blank=True)
    class Meta:
        db_table = u'ReferenceList'

    stateReferenceId =  ForeignKey(StatesMolecules, related_name='isStateRefId',
                                db_column='eId', null=False)

class Sources( Model):
    rId       =  IntegerField(primary_key=True, db_column='R_ID')
    authors   =  CharField(max_length=500, db_column='R_Authors', blank=True)
    category  =  CharField(max_length=100, db_column='R_Category', blank=True)
    name      =  CharField(max_length=200, db_column='R_SourceName', blank=True)
    year      =  IntegerField(null=True, db_column='R_Year', blank=True)
    vol       =  CharField(max_length=20, db_column='R_Volume', blank=True)
    doi       =  CharField(max_length=50, db_column='R_DOI', blank=True)
    pageBegin =  CharField(max_length=10, db_column='R_PageBegin', blank=True)
    pageEnd   =  CharField(max_length=10, db_column='R_PageEnd', blank=True)
    uri       =  CharField(max_length=100, db_column='R_URI', blank=True)
    publisher =  CharField(max_length=300, db_column='R_Publisher', blank=True)
    city      =  CharField(max_length=80, db_column='R_City', blank=True)
    editors   =  CharField(max_length=300, db_column='R_Editors', blank=True)
    productionDate =  DateField(max_length=12, db_column='R_ProductionDate', blank=True)
    version   =  CharField(max_length=20, db_column='R_Version', blank=True)
    comments  =  CharField(max_length=100, db_column='R_Comments', blank=True)
    class Meta:
        db_table = u'ReferenceBib'

    referenceId =  ForeignKey(SourcesIDRefs, related_name='isRefId',
                                db_column='rId', null=False)
