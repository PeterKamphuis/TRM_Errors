from dataclasses import dataclass, field
import psutil
from omegaconf import MISSING
from typing import List, Optional
import os
from TRM_errors.config.variables_config import Min_Errors,Variations
#The default total database currently make 229 galaxies
@dataclass
class Tirshaker:
    #tirshaker is the default
    enable: bool = True
    #The input def file for which to calculate the errors
    deffile_in: str = 'Finalmodel.def'
    deffile_out: str = 'Shaken_Errors.def'
    directory: str = 'Error_Shaker'
    #Do we want a log
    log: bool = False 
    mode: str = 'fitted' #Fitted the settings and grouping will be read from the fits file and def file if manual they have to be provided
    inimode: int=-1
    iterations: int=20
    individual_loops: int = -1  #Set this to -1 for final release
    tirific: str = 'tirific'

@dataclass
class General:
    input_cube: Optional[str] = None
    verbose: bool = True
    try:
        ncpu: int = len(psutil.Process().cpu_affinity())-1
    except AttributeError:
        ncpu: int = psutil.cpu_count()-1
   
    directory: str = os.getcwd()
    multiprocessing: bool = True
    calc_mode: str = 'mad'
    clean: bool = True
    #font_file: str = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
@dataclass
class defaults:
    print_examples: bool = False
    configuration_file: Optional[str] = None
    general: General = General()
    tirshaker: Tirshaker=Tirshaker()
    min_errors: Min_Errors = Min_Errors()
    variations: Variations = Variations() 
