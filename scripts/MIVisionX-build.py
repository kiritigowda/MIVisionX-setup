__author__      = "Kiriti Nagesh Gowda"
__copyright__   = "Copyright 2018, AMD Radeon MIVisionX build"
__license__     = "MIT"
__version__     = "0.9.5"
__maintainer__  = "Kiriti Nagesh Gowda"
__email__       = "Kiriti.NageshGowda@amd.com"
__status__      = "beta"

import os
import getopt
import sys
import subprocess
 

opts, args = getopt.getopt(sys.argv[1:], 's:d:l:')
 
sudoPassword = ''
buildDir = ''
linuxCMake = ''

for opt, arg in opts:
    if opt == '-s':
        sudoPassword = arg
    elif opt == '-d':
    	buildDir = arg
    elif opt =='-l':
		linuxCMake = arg

if sudoPassword == '':
    print('Invalid command line arguments.\n'\
    	  ' \t\t\t\t-s [sudo password - required]\n'\
    	  ' \t\t\t\t-l [Linux system cmake - optional (default:cmake options:cmake/cmake3)]\n '\
    	  ' \t\t\t\t-d [build directory - optional]\n ')
    exit()

if buildDir == '':
	buildDir_MIVisionX = '~/MIVisionX'
else:
	buildDir_MIVisionX = buildDir+'MIVisionX'


if linuxCMake == '' or linuxCMake == 'cmake':
	linuxCMake = 'cmake'
else:
	linuxCMake = 'cmake3'

# AMDOVX Work Flow
buildMain_dir = os.path.expanduser(buildDir_MIVisionX)
buildGIT_dir = os.path.expanduser(buildDir_MIVisionX+'/amdovx-modules')
buildMake_dir = os.path.expanduser(buildDir_MIVisionX+'/build')
if(os.path.exists(buildGIT_dir)):
	print("\nGit Folder Exist\n")
	os.system('(cd '+buildGIT_dir+'; git pull; git submodule init; git submodule update --recursive )');
else:
	os.system('rm -rf '+buildMain_dir);
	os.system('(cd ; mkdir '+buildMain_dir+')');
	os.system('(cd '+buildMain_dir+'; git clone --recursive http://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX )');
	os.system('(cd '+buildGIT_dir+'; git submodule init; git submodule update --recursive  )');

# AMDOVX Build
if(os.path.exists(buildMake_dir)):
	os.system('(cd '+buildMain_dir+'; rm -rf build)');
	os.system('(cd '+buildMain_dir+'; mkdir build)');
else:
	os.system('(cd '+buildMain_dir+'; mkdir build)');

os.system('(cd '+buildMake_dir+'; '+linuxCMake+' -DCMAKE_BUILD_TYPE=Release ../MIVisionX )');
os.system('(cd '+buildMake_dir+'; make -j8 )');
from subprocess import call
cmd='(cd '+buildMake_dir+'; sudo -S make install )'
call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
os.system('(cd '+buildMake_dir+'; ls -l bin )');
