__author__      = "Kiriti Nagesh Gowda"
__copyright__   = "Copyright 2018, AMD Radeon MIVisionX build"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Kiriti Nagesh Gowda"
__email__       = "Kiriti.NageshGowda@amd.com"
__status__      = "beta"

import argparse
import commands
import os

# Import arguments
parser = argparse.ArgumentParser()
parser.add_argument('--directory', 	type=str, default='',       help='build home directory - optional (default:~/)')
parser.add_argument('--cmake', 		type=str, default='cmake', 	help='Linux cmake - optional (default:cmake) [options: Ubuntu - cmake; CentOS - cmake3]')
args = parser.parse_args()

buildDir = args.directory
linuxCMake = args.cmake

if buildDir == '':
	buildDir_MIVisionX = '~/MIVisionX'
else:
	buildDir_MIVisionX = buildDir+'MIVisionX'

if linuxCMake == '' or linuxCMake == 'cmake':
	linuxCMake = 'cmake'
else:
	linuxCMake = 'cmake3'


# AMDOVX Work Flow
os.system('sudo -v')
buildMain_dir = os.path.expanduser(buildDir_MIVisionX)
buildGIT_dir = os.path.expanduser(buildDir_MIVisionX+'/MIVisionX')
buildMake_dir = os.path.expanduser(buildDir_MIVisionX+'/build')
if(os.path.exists(buildGIT_dir)):
	print("\nGit Folder Exist\n")
	os.system('(cd '+buildGIT_dir+'; git pull)')
else:
	os.system('rm -rf '+buildMain_dir)
	os.system('(cd ; mkdir '+buildMain_dir+')')
	os.system('(cd '+buildMain_dir+'; git clone https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX.git )')

# AMDOVX Build
if(os.path.exists(buildMake_dir)):
	os.system('(cd '+buildMain_dir+'; rm -rf build)')
	os.system('(cd '+buildMain_dir+'; mkdir build)')
else:
	os.system('(cd '+buildMain_dir+'; mkdir build)')

os.system('(cd '+buildMake_dir+'; '+linuxCMake+' -DCMAKE_BUILD_TYPE=Release ../MIVisionX )')
os.system('(cd '+buildMake_dir+'; make -j8 )')
os.system('(cd '+buildMake_dir+'; sudo -S make install )')
