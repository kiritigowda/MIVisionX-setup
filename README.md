[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# MIVisionX

This project contains scripts to setup, build, and profile AMD Radeon MIVisionX. The open source GitHub project can be found at [MIVisionX](https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX)

For convenience of the developer, we here provide the scripts which will install all the dependencies required by this project and clone the project from GitHub to build and install MIVisionX on your system.

## Prerequisites for running the script
1. Ubuntu `16.04`/`18.04` or CentOS `7.5`/`7.6`
2. [ROCm supported hardware](https://rocm.github.io/hardware.html)
3. [ROCm](https://github.com/RadeonOpenCompute/ROCm#installing-from-amd-rocm-repositories)

## scripts 
This folder has the following python scripts

1. **MIVisionX-setup.py** builds all the prerequisites required by MIVisionX. The setup script creates a deps folder and installs all the prerequisites, this script only needs to be executed once. If directory option is not given, the script will install deps folder in the home directory(~/) by default, else in the user specified location.

**usage:**
````
python MIVisionX-setup.py --directory [setup directory - optional]
                          --installer [Package management tool - optional (default:apt-get) [options: Ubuntu:apt-get;CentOS:yum]]
                          --miopen    [MIOpen Version - optional (default:1.7.0)]      
````
**Note:** use `--installer yum` for CentOS

2. **MIVisionX-build.py** - This script clones the latest MIVisionX from GitHub, builds and installs the project. If the -d build directory is not given the script creates a MIVisionX folder in the home/'~/' directory by default, else in the user-specified folder.

**usage:**
````
python MIVisionX-build.py --directory [setup directory - optional]
                          --cmake     [Linux cmake - optional (default:cmake) [options:Ubuntu - cmake; CentOS - cmake3]]  
````
**Note:** use `--cmake cmake3` for CentOS

## **Note** - `The steps below are only for developers with access to AMD developer server`

3. **MIVisionX-profile.py** - This script downloads the caffe .models & .prototxt from a remote file server and runs every model with different batch sizes and dumps an output.log file, profile.csv & profile.txt. The build directory should be the same director passed to the MIVision-build.py script. If no directory was given, pass '~/' for the directory option. 

usage:

````
python scripts/MIVision-profile.py  -d [build directory - required]
                                    -l [profile level - optional (level 1-8, default:7)]
                                    -m [profile mode - optional (level 1-6, default:2)]
                                    -f [MIOPEN_FIND_ENFORCE mode - optional (level 1-5, default:1)]
```` 

4. **MIVisionX-generatePlatformReport.py** - This Scripts generates the platfrom report for the system.

usage:

````
python scripts/MIVision-generatePlatformReport.py -d [build directory - required]
```` 

5. **MIVisionX-generateFullReport.py** - This Scripts generates the platfrom report & benchmark reports for the system.

usage:

````
python scripts/MIVision-generateFullReport.py -d [build directory - required]
```` 

## outputs
* The MIVision-profile.py will generate profile.txt and profile.csv.
* The MIVision-generatePlatformReport.py will generate platform report .md file.
* The MIVision-generateFullReport.py will generate platform and benchmark report .md file. A Diff report will be generated if the report was previously run on the same machine.
