[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# MIVisionX

This project contains scripts to setup, build, and profile AMD Radeon MIVisionX. The open source GitHub project can be found at [MIVisionX](https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX)


## Prerequisites for running the scripts
1. Ubuntu `16.04`/`18.04` or Centos `7.5`/`7.6`
2. [ROCm supported hardware](https://rocm.github.io/hardware.html)
3. [ROCm](https://github.com/RadeonOpenCompute/ROCm#installing-from-amd-rocm-repositories)

## scripts 
This folder has the following python scripts

1. **MIVisionX-setup.py** - This script builds all the prerequisites required by MIVisionX. The setup script creates a deps folder and installs all the prerequisites, this script only needs to be executed once. If -d option for the directory is not given the script will install deps folder in '~/' directory by default, else in the user-specified folder.

usage:

````
python mivisionx-setup/scripts/MIVisionX-setup.py -s [sudo password - required]
                                                  -d [setup directory - optional]
                                                  -l [Linux system install - optional (default:apt-get options:apt-get/yum)]
                                                  -m [MIOpen Version - optional (default:1.6.0)]
```` 

2. **MIVisionX-build.py** - This script clones the latest MIVisionX from GitHub, builds and installs the project. If the -d build directory is not given the script creates a MIVisionX folder in the home/'~/' directory by default, else in the user-specified folder.

usage:

````
python mivisionx-setup/scripts/MIVisionX-build.py   -s [sudo password - required]
                                                    -l [Linux system cmake - optional (default:cmake options:cmake/cmake3)]
                                                    -d [build directory - optional]
```` 

*Note* - `The steps below are only for developers with access to AMD developer server`

3. **MIVisionX-profile.py** - This script downloads the caffe .models & .prototxt from a remote file server and runs every model with different batch sizes and dumps an output.log file, profile.csv & profile.txt. The build directory should be the same director passed to the MIVision-build.py script. If no directory was given, pass '~/' for the directory option. 

usage:

````
python MIVision-profile.py  -d [build directory - required]
                            -l [profile level - optional (level 1-8, default:7)]
                            -m [profile mode - optional (level 1-6, default:2)]
                            -f [MIOPEN_FIND_ENFORCE mode - optional (level 1-5, default:1)]
```` 

4. **MIVisionX-generatePlatformReport.py** - This Scripts generates the platfrom report for the system.

usage:

````
python MIVision-generatePlatformReport.py -d [build directory - required]
```` 

5. **MIVisionX-generateFullReport.py** - This Scripts generates the platfrom report & benchmark reports for the system.

usage:

````
python MIVision-generateFullReport.py -d [build directory - required]
```` 

## outputs
* The MIVision-profile.py will generate profile.txt and profile.csv.
* The MIVision-generatePlatformReport.py will generate platform report .md file.
* The MIVision-generateFullReport.py will generate platform and benchmark report .md file. A Diff report will be generated if the report was previously run on the same machine.
