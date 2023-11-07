# TRM_Errors

=====

Introduction
------------

A pyhon package to create  errors for Tilted Ring Models. Version 0.0.4 is the first fully working version that incorporates the tirshaker module as written by G.I.G. J\'ozsa.

Requirements
------------
The code requires full installation of:

    python v3.6 or higher
    tirific


[python](https://www.python.org/),[TiRiFiC](http://gigjozsa.github.io/tirific/download_and_installation.html)


Installation
------------

Download the source code from the Github or simply install with pip as:

  	pip install TRM_errors

This should also install all required python dependencies.
We recommend the use of python virtual environments. If so desired a TRM_errors installation would look like:

  	python3 -m venv TRM_errors_venv

  	source TRM_errors_venv/bin/activate.csh

    pip install TRM_errors

(In case of bash the correct middle line is 	source TRM_errors_venv/bin/activate)
You might have to restart the env:

  	deactivate

  	source TRM_errors_venv/bin/activate.csh

Once you have installed FAT you can check that it has been installed properly by running FAT as.

  	create_TRM_errors -v 


Running TRM_errors
------------------

You can run TRM_errors by providing a configuration file by 

create_TRM_errors configuration_file=file.yml

an example yaml file with all parameters can be printed by running

create_TRM_errors print_examples=true 

please see the advanced input in readthe docs for an explanation of all parameters.