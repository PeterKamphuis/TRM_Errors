# -*- coding: future_fstrings -*-

# This is the stand alone version of the pyFAT moments to create moment maps

#from optparse import OptionParser
from omegaconf import OmegaConf
from TRM_Errors.config.config import defaults
from TRM_Errors.tirshaker.tirshaker import run_tirshaker
import numpy as np
import sys
import os
import traceback
import warnings
import TRM_Errors
import psutil



def warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file,'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))





def main(argv):
    if '-v' in argv or '--version' in argv:
        print(f"This is version {TRM_Errors.__version__} of the program.")
        sys.exit()

    if '-h' in argv or '--help' in argv:
        print('''
Use TRM_Errors in this way:

All config parameters can be set directly from the command line by setting the correct parameters, e.g:
create_TRM_errors def_file=cube.fits error_generator=tirshaker 
''')
        sys.exit()


    cfg = OmegaConf.structured(defaults)
    if cfg.general.ncpu == psutil.cpu_count():
        cfg.general.ncpu -= 1
    inputconf = OmegaConf.from_cli(argv)
    cfg_input = OmegaConf.merge(cfg,inputconf)
    
    if cfg_input.print_examples:
        with open('default.yml','w') as default_write:
            default_write.write(OmegaConf.to_yaml(cfg))
        print(f'''We have printed the file default.yml in {os.getcwd()}.
Exiting moments.''')
        sys.exit()

    if cfg_input.configuration_file:
        succes = False
        while not succes:
            try:
                yaml_config = OmegaConf.load(cfg_input.configuration_file)
        #merge yml file with defaults
                cfg = OmegaConf.merge(cfg,yaml_config)
                succes = True
            except FileNotFoundError:
                cfg_input.configuration_file = input(f'''
You have provided a config file ({cfg_input.configuration_file}) but it can't be found.
If you want to provide a config file please give the correct name.
Else press CTRL-C to abort.
configuration_file = ''')
    cfg = OmegaConf.merge(cfg,inputconf) 
    if cfg.tirshaker.enable:
        run_tirshaker(cfg)




if __name__ =="__main__":
    main()
