#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program implements a database importer that reads from
ascii-input files to the django database. It's generic and is
controlled from a mapping file.

This is the working methods.

"""
import sys
from django.db.models import Q
from time import time 

#from django.db.utils import IntegrityError
#import string as s

TOTAL_LINES = 0
TOTAL_ERRS = 0

# Line functions

def charrange(linedata, start, end, filenum=0):
    """
    Cut out part of a line of texts based on indices
    """
    try:
        return linedata[filenum][start:end].strip()
    except Exception, e:
        pass
        #print "charrange skipping '%s': %s" % (linedata, e)
    
def charrange2int(linedata, start, end, filenum=0):
    try:
        return int(round(float(charrange(linedata[filenum], start, end))))
    except Exception:
        pass
    
def bySepNr(linedata, number, sep=',',filenum=0):
    """
    Split a text line by sep argument and return
    the split section with given number
    """
    try:
        return linedata[filenum].split(sep)[number].strip()
    except Exception, e:
        pass
        #print "bySepNr skipping line '%s': %s" % (linedata, e)

def chainCmds(linedata, *linefuncs):
    """
    This command allows for chaining together several line functions in
    sequence. The results of the first function will be passed to the second
    one etc.

    linefuncs should be a list [(func1, (arg1,arg2,...)), (func2,(arg1,arg2,..)),...]
    """

    data = linedata
    for func, args in linefuncs:
        data = [func(data, *args)]
    if data:
        return data[0]
    #print "chainCommands skipping line." 
         
def idFromLine(linedata, sep, *linefuncs):
    """
    Extract strings from a line in order to build a unique id-string,
    using one or more line functions to extract parts of a line and
    paste them together with a separator given by 'sep'.
    The line functions must be stored as tuples (func, (arg1,arg2,..)). 

    Example of call:
      idFromLine('-', (bySepNr,(3,';'), (charrange2int,(45,67))) )    
    """
    #print linedata
    #pdb.set_trace()
    if not sep:
        sep = "-"
    dbref = []
    for func, args in linefuncs:
        string = str(func(linedata, *args)).strip()        
        if not string:
            string = sep
        #print string 
        dbref.append(string)
    #print sep.join(dbref)
    return sep.join(dbref)



# Helper methods for parsing and displaying 

def is_iter(iterable):
    """
    Checks if an object behaves iterably. 
    Strings are not accepted as iterable (although
    they are actually iterable), since string iterations
    are usually not what we want to do with a string.
    """
    if isinstance(iterable, basestring):
        # skip all forms of strings (str, unicode etc)
        return False     
    try:
        # check if object implements iter protocol
        return iter(iterable)
    except TypeError:
        return False 

def ftime(t0, t1):
    "formats time to nice format."
    ds = t1 - t0
    dm, ds = int(ds) / 60, ds % 60
    return "%s min, %s s." % (dm, ds)

def log_trace(e, info=""):
    """
    Intended to be called from inside a traceback exception with
    the exception object as first argument.
    Captures the latest traceback. 
    """
    sys.stderr.write("%s%s\n" % (info, str(e)))

def read_mapping(fname):
    """
    Read the config dictionary from a file.
    Note: very unsafe, since the content gets executed.
    Have a look at createcfg() to see how it should look like.
    """
    try:
        f=open(fname)
    except IOError:
        print "Error: File name '%s' not found." % fname
        return None
    exec(f.read()) # this should define a variable "mapping"
    try:
        return mapping
    except NameError:
        print "Error: mapping_file must contain a global variable called 'mapping'."
        return None

def validate_mapping(mapping):
    """
    Check the mapping definition to make sure it contains
    a structure suitable for the parser.
    """
    required_fdict_keys = ("model", "fname", "headlines", "commentchar", "linemap")
    required_col_keys = ("cname", "cbyte")
    if not mapping:
        raise Exception("Empty/malformed mapping.")
    if not type(mapping) == list or \
           any([True for fdict in mapping if type(fdict) != dict]): 
        raise Exception("Mapping must be a list of dictionaries, one for each file to convert.")
    for fdict in mapping: 
        if len([True for key in fdict.keys() if key in required_fdict_keys]) < len(required_fdict_keys):
            string = "Mapping error: One of the keys %s is missing from the mapping %s."
            raise Exception(string % (required_fdict_keys, fdict.keys()))
        if not fdict['linemap'] or type(fdict['linemap']) != list:
            raise Exception("Mapping error: 'linemap' must be a list of dicts.")     
        for col in fdict['linemap']:            
            if not type(col) == dict or \
                len([True for key in col.keys()
                     if key in required_col_keys]) < len(required_col_keys):
                string = "Mapping error: Linemaps must have at least keys %s" 
                raise Exception(string % required_col_keys)
    return True 


# working functions for the importer
    
def process_line(linedata, column_dict):
    """
    Process one line of data. Linedata is a tuple that always starts with
    the raw string for the line.    
    """
    colfunc = column_dict['cbyte'][0]
    args = column_dict['cbyte'][1]
    try:        
        dat = colfunc(linedata,  *args)
    except Exception, e:
        log_trace(e, "error processing lines '%s' - in %s%s: " % (linedata, colfunc, args))
        raise 
    if not dat or (column_dict.has_key('cnull') \
                   and dat == column_dict['cnull']):
        return None
    return dat

def get_model_instance(tconf, line, model):
    """
    Get model instance to update, alternatively create new model
    """
    if tconf.has_key('updatematch'):
        # we want to update an existing model instance.
        dat = process_line(line, tconf['columns'][0])
        if not dat:
            return
        # this defines 'modelq' as a queryset
        exec('modelq=Q(%s="%s")' % (tconf['updatematch'], dat))
        try:
             data = model.objects.get(modelq)
        except Exception:
            data = None
    else: 
        # create a new instance of the model
        data=model()
    return data
                    
def find_match_and_update(property_name, match_key, model, data):
    """
    Don't create a new database object, instead search
    the database and update an existing one.
    """       
        
    # this instantiates 'modelq' as a queryset 
    modelq = eval('Q(%s="%s")' % (property_name, match_key))
    
    try:
        match = model.objects.get(modelq) 
    except Exception, e:
        raise Exception("%s: Q(%s=%s)" % (e, property_name, match_key))
    # set variables on the object
    for key in (key for key in data.keys() if key != match_key):     
        try:
            setattr(match, key, data[key])
            match.save(force_update=True) 
        except Exception, e:
            sys.stderr.write("%s: model.%s=%s\n" % (e, key, data[key]))
            
def create_new(model, data):
    """
    Create a new object of type model and store
    it in the database.

    model - django model type
    inpdict - dictionary of fieldname:value that should be created.
    """
    model.objects.create(**data)

class MappingFile(object):
    """
    This class implements an object that represents
    an open file from which one can read lines. The object
    keeps track of its own line-step speed and will return lines
    as defined by this speed. E.g. for a line-step speed of 0.5,
    it will return the same line twice in a row whereas for a
    step speed of 2, will return every second line etc. 
    """
    def __init__(self, filepath, headlines, commentchar, lineoffset, linestep, errline):
        "Initialize the file"

        self.commentchar = commentchar
        self.file = open(filepath, 'r')
        self.lines = self.file.xreadlines() # a generator
        for i in range(headlines + lineoffset):
            self.lines.next()
        while True:
            self.line = self.lines.next()
            if not self.line.startswith(self.commentchar):
                break 
        self.counter = -linestep
        self.linestep = linestep
        self.errline = str(errline)
        
    def readline(self):
        """
        Return a line from the file.

        This method understand both slower
        line stepping (0 < linestep < 1) and faster (> 1)
        """
        self.counter += self.linestep
        if self.counter == 0:          
            # always return the first line
            return self.line                
        elif self.counter % 1 == 0:
            # only step if counter equals an even line
            for i in range(max(1, self.linestep)):                
                while True:
                    self.line = self.lines.next()
                    if not self.line.startswith(self.commentchar):
                        break        
        if self.line.startswith(self.errline):            
            self.line = ""
        return self.line
    
def parse_file_dict(file_dict, debug=False):
    """
    Process one file definition from a config dictionary by
    processing the file name stored in it and parse it according
    to the mapping. 

    file_dict - config dictionary representing one input file structure
    (for an example see e.g. mapping_vald3.py)
    """    

    # parsing the file/model info. Everything except
    # the mode is always an iterable.

    # model specific 
    
    # model to work on
    model = file_dict['model']    
    mapping = file_dict['linemap']
    # update an existing model using field named updatematch
    updatematch = file_dict.get('updatematch', None) 

    # file specifics 
    
    filepaths = file_dict['fname']
    if not is_iter(filepaths):
        filepaths = [filepaths]
    nfiles = len(filepaths)
    filenames = [path.split('/')[-1] for path in filepaths]

    headlines = file_dict['headlines']
    if not is_iter(headlines):
        headlines = [headlines]
    commentchars = file_dict['commentchar']
    if not is_iter(commentchars):
        commentchars = [commentchars]       
    # optional  
    linesteps = file_dict.get('linestep', [1 for i in range(nfiles)])
    if not is_iter(linesteps):
        linesteps = [linesteps]
    lineoffsets = file_dict.get('lineoffset', [0 for i in range(nfiles)])
    if not is_iter(lineoffsets):
        lineoffsets = [lineoffsets]
    # lines that are identified as bad
    errlines = file_dict.get('errlines', ["Unknown" for i in range(nfiles)])
    if not is_iter(errlines):
        errlines = [errlines]
    
    # -----
        
    if len(filenames) == 1:
        print 'Working on %s ...' % filenames[0]
    else:
        print "Working on " + " + ".join(filenames) + " ..." 

    # open file handles
    mapfiles = []
    for fnum, filepath in enumerate(filepaths):
        mapfiles.append(MappingFile(filepath, headlines[fnum], commentchars[fnum],
                                    lineoffsets[fnum], linesteps[fnum], errlines[fnum]))
    data = {}
    total = 0
    errors = 0   
    while True:
        # step and read one line from all files 
        total += 1
        lines = []
        try:
            for mapfile in mapfiles:
                # this automatically syncs all files' lines
                lines.append(mapfile.readline())
        except StopIteration:
            # we are done.
            break 
                            
        for map_dict in mapping:

            # parse the mapping for this line(s)
            dat = process_line(lines, map_dict)           
            if not dat or (map_dict.has_key('cnull') 
                   and dat == map_dict['cnull']):
                # not a valid line for whatever reason 
                continue

            if map_dict.has_key('references'):
                # this collumn references another field
                # (i.e. a foreign key)
                refmodel = map_dict['references'][0]
                refcol = map_dict['references'][1]            
                # create a query object q for locating
                # the referenced model and field
                Qquery = eval('Q(%s="%s")' % (refcol, dat))
                try:
                    dat = refmodel.objects.get(Qquery)
                except Exception:
                    errors += 1
                    if len(map_dict['references']) > 2 \
                            and map_dict['references'][2] == 'skiperror':
                        # Don't create an entry for this (this requires
                        # null=True in the relevant field)
                        if debug:
                            print "skipping unfound reference %s" % dat
                        continue
                    # this is a real error, should always stop.
                    string = "reference %s.%s='%s' not found.\n"                     
                    print string % (refmodel,refcol, dat)
                    raw_input("paused...")
                    dat = None            

            data[map_dict['cname']] = dat

            # line columns parsed; now move to database 

        if updatematch:
            # Model was already created; this run is for
            # updating it properly (e.g. for vald)            
            try:
                match_key = data[updatematch]
                find_match_and_update(updatematch, match_key, model, data)
            except Exception, e:
                errors += 1
                if debug:
                    log_trace(e, "ERROR updating %s: " % model)
                
        else:
            # create a new instance of model and store it in database,
            # populated with the relevant fields. 
            if not data.has_key('pk'):
                data['pk'] = None
            try:
                create_new(model, data)
            except Exception, e:                
                errors += 1
                if debug:
                    log_trace(e, "ERROR creating %s: " % model)

    print '%s done. %i collisions/errors/nomatches out of %i lines.' % (" + ".join(filenames), errors, total)

    global TOTAL_LINES, TOTAL_ERRS
    TOTAL_LINES += total
    TOTAL_ERRS += errors
    
def parse_mapping(mapping, debug=False):
    """
    Step through a list of mappings describing
    the relation between (usually ascii-)files and
    django database fields. This should ideally
    not have to be changed for different database types.
    """
    import gc, pdb
    if validate_mapping(mapping):    
        t0 = time()
        gc.DEBUG_SAVEALL = True
        import cProfile as profile
        for file_dict in mapping:
            t1 = time()            
            parse_file_dict(file_dict, debug=debug)
            print "Time used: %s" % ftime(t1, time())
            #pdb.set_trace()
            #print gc.garbage
            #print gc.get_count()
        
        print "Total time used: %s" % ftime(t0, time())
        print "Total number of errors/fails/skips: %s/%s (%g%%)" % (TOTAL_ERRS,
                                                                TOTAL_LINES,
                                                                100*float(TOTAL_ERRS)/TOTAL_LINES)
