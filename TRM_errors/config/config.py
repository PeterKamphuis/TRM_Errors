from dataclasses import dataclass, field
from multiprocessing import cpu_count
from omegaconf import MISSING
from typing import List, Optional
import os

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
    ncpu: int = cpu_count()-1
    directory: str = os.getcwd()
    multiprocessing: bool = True
    calc_mode: str = 'mad'
    clean: bool = True
    #font_file: str = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"

@dataclass
class Min_Errors:
    PA: float = 0.
    INCL: float = 0.
    VROT: float = 0.
    VRAD: float = 0.
    VSYS: float = 0.
    XPOS: float = 0.
    YPOS: float = 0.
    SBR: float = 0.
    Z0: float = 0.
    SDIS: float = 0.   
   


@dataclass
class Variations:
    VARY: str = '!VROT VROT_2'    # Set the parameters manually, if ! causes problems use i 
    PA: List = field(default_factory=lambda: [10, 'unit','angle','a'])    #unit is as unit in program, res is times resolution of the cube
    INCL: List = field(default_factory=lambda: [10, 'unit','angle', 'a'])
    VROT: List = field(default_factory=lambda: [5, 'res','km/s','a'])
    VRAD: List = field(default_factory=lambda: [2.5, 'res','km/s','a'])    #unit is as unit in program, res is times resolution of the cube
    VSYS: List = field(default_factory=lambda: [0.1, 'res','km/s', 'a'])
    XPOS: List = field(default_factory=lambda: [0.3, 'res','degree','a'])
    YPOS: List = field(default_factory=lambda: [0.3, 'res','degree','a'])    #unit is as unit in program, res is times resolution of the cube
    SBR: List = field(default_factory=lambda: [1e-4, 'unit','jy/arcsec^2', 'a'])
    Z0: List = field(default_factory=lambda: [1, 'res','arcsec','a'])
    SDIS: List = field(default_factory=lambda: [2, 'res','km/s','a'])    #unit is as unit in program, res is times resolution of the cube
  

@dataclass
class defaults:
    print_examples: bool = False
    configuration_file: Optional[str] = None
    general: General = General()
    tirshaker: Tirshaker=Tirshaker()
    min_errors: Min_Errors = Min_Errors()
    variations: Variations = Variations() 
