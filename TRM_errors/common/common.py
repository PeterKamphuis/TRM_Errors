# -*- coding: future_fstrings -*-
# Functions common ly used

import os
import numpy as np
import traceback
import signal
import psutil

from collections import OrderedDict

class InputError(Exception):
    pass
class ProgramError(Exception):
    pass

# A class of ordered dictionary where keys can be inserted in at specified locations or at the end.
class Proper_Dictionary(OrderedDict):
    def __setitem__(self, key, value):
        if key not in self:
            # If it is a new item we only allow it if it is not Configuration or Original_Cube or if we are in setup_configuration
            try:
                function,variable,empty = traceback.format_stack()[-2].split('\n')
            except ValueError: 
                function,variable = traceback.format_stack()[-2].split('\n')
            function = function.split()[-1].strip()
            variable = variable.split('[')[0].strip()
            if variable == 'Original_Configuration' or variable == 'Configuration':
                if function != 'setup_configuration':
                    raise ProgramError("FAT does not allow additional values to the Configuration outside the setup_configuration in support_functions.")
        OrderedDict.__setitem__(self,key, value)
    #    "what habbens now")
    def insert(self, existing_key, new_key, key_value):
        done = False
        if new_key in self:
            self[new_key] = key_value
            done = True
        else:
            new_orderded_dict = self.__class__()
            for key, value in self.items():
                new_orderded_dict[key] = value
                if key == existing_key:
                    new_orderded_dict[new_key] = key_value
                    done = True
            if not done:
                new_orderded_dict[new_key] = key_value
                done = True
                print(
                    f"----!!!!!!!! YOUR {new_key} was appended at the end as you provided the non-existing {existing_key} to add it after!!!!!!---------")
            self.clear()
            self.update(new_orderded_dict)

        if not done:
            print("----!!!!!!!!We were unable to add your key!!!!!!---------")

Proper_Dictionary.__doc__=f'''
A class of ordered dictionary where keys can be inserted in at specified locations or at the end.
'''


def check_cpu(cfg):
    '''Check that the amount of cpus is not exceeding the maximum available'''
    try:
        max_ncpu: int = len(psutil.Process().cpu_affinity())-1
    except AttributeError:
        max_ncpu: int = psutil.cpu_count()-1
    if cfg.general.ncpu > max_ncpu:
        cfg.general.ncpu = max_ncpu
    return cfg

def check_pid(pid):        
    """ Check whether titific is running. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
    
    
    
def finish_current_run(current_run,log= False):
    log_statement = ''
    if check_pid(current_run.pid):
        try:
            current_run.stdout.close()
            current_run.stderr.close()
        except:
            log_statement += print_log(f'''FINISH_CURRENT_RUN: We failed to close the pipe to the current run even though there should be one.
''',log)
            pass
        try:
            os.kill(current_run.pid, signal.SIGKILL)
            log_statement += print(f'''FINISH_CURRENT_RUN: We killed PID = {current_run.pid}.
''',log)
        except:
            try:
                current_run.kill()
                log_statement += print_log(f'''FINISH_CURRENT_RUN: We killed the current run although we failed on the PID = {current_run.pid}.
''',log)
            except AttributeError:
                log_statement += print_log(f'''FINISH_CURRENT_RUN: We failed to kill the current run with PID {current_run.pid} even though we have tirific running
''',log)
                raise ProgramError('FINISH_CURRENT_RUN: Despite having an initialized tirific we could not kill it. This should not happen.')
     
    else:
        log_statement += print_log(f'''FINISH_CURRENT_RUN: No run is initialized.
''',log)
    return log_statement
finish_current_run.__doc__ =f'''
 NAME:
    finish_current_run
 PURPOSE:
    make sure that the initiated tirific is cleaned when pyFAT stops
 CATEGORY:
    support_functions

 INPUTS:
    Configuration = Standard FAT configuration
    current_run = subprocess structure for the current tirific run

 OPTIONAL INPUTS:


 OUTPUTS:
    kills tirific if initialized or raises an error when it fails to do so while tirific is running

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''

def load_tirific(def_input,Variables = None,array = False,\
        ensure_rings = False ,dict=False, template = False):
    #Cause python is the dumbest and mutable objects in the FAT_defaults
    # such as lists transfer
    if Variables == None:
        Variables = ['BMIN','BMAJ','BPA','RMS','DISTANCE','NUR','RADI',\
                     'VROT','Z0', 'SBR', 'INCL','PA','XPOS','YPOS','VSYS',\
                     'SDIS','VROT_2',  'Z0_2','SBR_2','INCL_2','PA_2','XPOS_2',\
                     'YPOS_2','VSYS_2','SDIS_2','CONDISP','CFLUX','CFLUX_2']


    # if the input is a string we first load the template
    if isinstance(def_input,str):
        def_input = tirific_template(filename = def_input )

    out = []
    for key in Variables:

        try:
            out.append([float(x) for x  in def_input[key].split()])
        except KeyError:
            out.append([])
        except ValueError:
            out.append([x for x  in def_input[key].split()])

    #Because lists are stupid i.e. sbr[0][0] = SBR[0], sbr[1][0] = SBR_2[0] but  sbr[:][0] = SBR[:] not SBR[0],SBR_2[0] as logic would demand

    if array:
        tmp = out
        #We can ensure that the output has the same number of values as there are rings
        if ensure_rings:
            length=int(def_input['NUR'])
        else:
            #or just take the longest input as the size
            length = max(map(len,out))
        #let's just order this in variable, values such that it unpacks properly into a list of variables
        out = np.zeros((len(Variables),length),dtype=float)
        for i,variable in enumerate(tmp):
            if len(variable) > 0.:
                out[i,0:len(variable)] = variable[0:len(variable)]

    if dict:
        tmp = {}
        for i,var in enumerate(Variables):
            tmp[var] = out[i]
        out = tmp
    elif len(Variables) == 1:
        out= out[0]
    #print(f'''LOAD_TIRIFIC: We extracted the following profiles from the Template.
#{'':8s}Requested Variables = {Variables}
#{'':8s}Extracted = {out}
#''')
    #Beware that lists are stupid i.e. sbr[0][0] = SBR[0], sbr[1][0] = SBR_2[0] but  sbr[:][0] = SBR[:] not SBR[0],SBR_2[0] as logic would demand
    # However if you make a np. array from it make sure that you specify float  or have lists of the same length else you get an array of lists which behave just as dumb

    return out
load_tirific.__doc__ =f'''
 NAME:
    load_tirific

 PURPOSE:
    Load values from variables set in the tirific files

 CATEGORY:
    common_functions

 INPUTS:
    def_input = Path to the tirific def file or a FAT tirific template dictionary

 OPTIONAL INPUTS:
    Variables = ['BMIN','BMAJ','BPA','RMS','DISTANCE','NUR','RADI','VROT',
                 'Z0', 'SBR', 'INCL','PA','XPOS','YPOS','VSYS','SDIS','VROT_2',  'Z0_2','SBR_2',
                 'INCL_2','PA_2','XPOS_2','YPOS_2','VSYS_2','SDIS_2','CONDISP','CFLUX','CFLUX_2']


    array = False
        Specify that the output should be an numpy array with all varables having the same length

    ensure_rings =false
        Specify that the output array should have the length of the NUR parameter in the def file

    dict = False
        Return the output as a dictionary with the variable names as handles
 OUTPUTS:
    outputarray list/array/dictionary with all the values of the parameters requested

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
    This function has the added option of a dictionary compared to pyFAT
'''

def print_log(log_statement,log=False): 
    if log:
        return log_statement
    else: 
        print(log_statement)
        return ''


def set_format(key):   
    key = key.split('_')[0]
    if key in ['SBR', 'SBR_2']:
        format = '.5e'
    elif key in ['XPOS', 'YPOS','XPOS_2', 'YPOS_2']:
        format = '.7e'
    else:
        format = '.2f'
    return format

set_format.__doc__ =f'''
 NAME:
    set_format

 PURPOSE:
    Get the format code for specific tirific parameter

 CATEGORY:
    support_functions

 INPUTS:
    key = Tirific parameter to get code for

 OPTIONAL INPUTS:

 OUTPUTS:
    The format code

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''



def set_limits(value,minv,maxv):
    if value < minv:
        return minv
    elif value > maxv:
        return maxv
    else:
        return value


def tirific_template(filename = ''):
    if filename == '':
        raise InputError(f'Tirific_Template does not know a default')
    else:
        with open(filename, 'r') as tmp:
            template = tmp.readlines()
    result = Proper_Dictionary()
    counter = 0
    # Separate the keyword names
    for line in template:
        key = str(line.split('=')[0].strip().upper())
        if key == '':
            result[f'EMPTY{counter}'] = line
            counter += 1
        else:
            result[key] = str(line.split('=')[1].strip())
    return result
tirific_template.__doc__ ='''
 NAME:
    tirific_template

 PURPOSE:
    Read a tirific def file into a dictionary to use as a template.
    The parameter ill be the dictionary key with the values stored in that key

 CATEGORY:
    read_functions

 INPUTS:
    filename = Name of the def file

 OPTIONAL INPUTS:
    filename = ''
    Name of the def file, if unset the def file in Templates is used



 OUTPUTS:
    result = dictionary with the read file

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
      split, strip, open

 NOTE:
'''


def write_tirific(Tirific_Template, name = 'tirific.def',\
                full_name = False  ):
    if 'RESTARTID' in Tirific_Template:
        Tirific_Template['RESTARTID'] = str(int(Tirific_Template['RESTARTID'])+1)
   
    if full_name:
        file_name = name
    else:
        current_dir = os.getcwd()
        file_name = f'{current_dir}/{name}'
    with open(file_name, 'w') as file:
        for key in Tirific_Template:
            if key[0:5] == 'EMPTY':
                file.write('\n')
            else:
                file.write((f"{key}= {Tirific_Template[key]} \n"))
write_tirific.__doc__ =f'''
 NAME:
    tirific

 PURPOSE:
    Write a tirific template to file

 CATEGORY:
    write_functions

 INPUTS:
    Configuration = Standard FAT configuration
    Tirific_Template = Standard FAT Tirific Template

 OPTIONAL INPUTS:


    name = 'tirific.def'
    name of the file to write to

 OUTPUTS:
    Tirific def file

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
 '''