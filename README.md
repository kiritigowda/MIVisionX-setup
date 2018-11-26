[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# MIVisionX 

This project contains scripts to setup, build, and profile AMD Radeon MIVisionX. The open source GitHub project can be found at [MIVisionX](https://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-modules)


## Prerequisites for running the scripts
1. ubuntu 16.04/18.04
2. [ROCm supported hardware](https://rocm.github.io/hardware.html)
3. [ROCm](https://github.com/RadeonOpenCompute/ROCm#installing-from-amd-rocm-repositories)

## scripts 
This folder has the following python scripts

1. **MIVision-setup.py** - This scipts builds all the prerequisites required by MIVisionX. The setup script creates a deps folder and installs all the prerequisites, this script only needs to be executed once. If -d option for directory is not given the script will install deps folder in '~/' directory by default, else in the user specified folder.

usage:

````
python MIVision-setup.py -s [sudo password - required] -d [setup directory - optional]
```` 

2. **MIVision-build.py** - This script clones the latest MIVisionX from github, builds and installs the project. If the -d build directory is not given the script creates a MIVisionX folder in the home/'~/' directory by default, else in the user specified folder.

usage:

````
python MIVision-build.py -s [sudo password - required] -d [build directory - optional]
```` 

3. **MIVision-profile.py** - This script downloads the caffe .models & .prototxt from a remote file server and runs every model with different batch sizes and dumps an output.log file, profile.csv & profile.txt. The build directory should be the same director passed to the MIVision-build.py script. If no directory was given, pass '~/' for the directory option. 

usage:

````
python MIVision-profile.py -d [build directory - required] -l [profile level - optional (1-8, default:7)] -m [Profile Mode - optional (1-6, default:2)]
```` 

4. **MIVision-generatePlatformReport.py** - This Scripts generates the platfrom report for the system.

usage:

````
python MIVision-generatePlatformReport.py -d [build directory - required]
```` 

5. **MIVision-generateFullReport.py** - This Scripts generates the platfrom report & benchmark reports for the system.

usage:

````
python MIVision-generateFullReport.py -d [build directory - required]
```` 

## outputs
* The MIVision-profile.py will generate profile.txt and profile.csv.
* The MIVision-generatePlatformReport.py will generate platform report .md file.
* The MIVision-generateFullReport.py will generate platform and benchmark report .md file. A Diff report will be generated if the report was previously run on the same machine.
