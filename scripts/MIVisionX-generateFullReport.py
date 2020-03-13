__author__      = "Kiriti Nagesh Gowda"
__copyright__   = "Copyright 2018-2020, AMD MIVision Generate Full Report"
__credits__     = ["Aguren, Derrick"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Kiriti Nagesh Gowda"
__email__       = "Kiriti.NageshGowda@amd.com"
__status__      = "Shipping"

import os
import getopt
import sys
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

opts, args = getopt.getopt(sys.argv[1:], 'd:m:')

buildDir = ''
profileMode = 0

for opt, arg in opts:
    if opt == '-d':
        buildDir = arg
    elif opt =='-m':
        profileMode = int(arg)

if buildDir == '':
    print('Invalid command line arguments.\n \t\t\t\t-d [build directory - required]\n ')
    exit()

if buildDir == '':
    buildDir_MIVisionX = '~/MIVisionX'
else:
    buildDir_MIVisionX = buildDir+'MIVisionX'

AMDOVX_dir = os.path.expanduser(buildDir_MIVisionX)

if profileMode == 0:
    profileMode = 1


def shell(cmd):

    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output = p.communicate()[0][0:-1]

    return output

def write_formatted(output, f):

    f.write("````\n")
    f.write("%s\n\n" % output)
    f.write("````\n")

def write_lines_as_table(header, lines, f):

    for h in header:
        f.write("|%s" % h)

    f.write("|\n")

    for h in header:
        f.write("|:---")

    f.write("|\n")

    for l in lines:
        fields = l.split()
        for field in fields:
            f.write("|%s" % field)
        f.write("|\n")

def strip_libtree_addresses(lib_tree):

    return lib_tree

if __name__ == "__main__":

    # report configuration
    out_filename_time = False
    if profileMode == 1:
        path_to_so = buildDir_MIVisionX+'/develop/caffe-folder/googlenet/nnir_build_1/libannmodule.so'
    else:
        print("\nERROR - Dynamic Library List Implemented only for MODE-1 : OTHER MODES TBD\n")


    # get system data
    platform_name = shell('hostname')
    platform_name_fq = shell('hostname --all-fqdns')
    platform_ip = shell('hostname -I')[0:-1] # extra trailing space

    if out_filename_time:
        file_dtstr = datetime.now().strftime("%Y%m%d-%H%M%S")
    else:
        file_dtstr = datetime.now().strftime("%Y%m%d")

    report_filename = 'full_report_%s_%s.md' % (platform_name, file_dtstr)

    report_dtstr = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

    sys_info = shell('inxi -c0 -S')

    cpu_info = shell('inxi -c0 -C')
    cpu_info = cpu_info.split('\n')[0] # strip out clock speeds

    gpu_info = shell('inxi -c0 -G')
    gpu_info = gpu_info.split('\n')[0] # strip out X info

    memory_info = shell ('sudo inxi -c 0 -m')
    board_info = shell('inxi -c0 -M')

    lib_tree = shell('ldd -v %s' % path_to_so)
    lib_tree = strip_libtree_addresses(lib_tree)

    vbios = shell('(cd /opt/rocm/bin/; ./rocm-smi -v)')

    rocmInfo = shell('(cd /opt/rocm/bin/; ./rocm-smi -a)')

    rocm_packages = shell('dpkg-query -W | grep rocm').split('\n')    

    # write report
    if profileMode == 1:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("MIVisionX Neural Net Performance Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/caffe2nnir2openvx_noFuse_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm Package and Version Report\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios Report\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm Device Info Report\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries Report\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018 - 2020\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');

    elif profileMode == 2:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("Full Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/caffe2nnir2openvx_fuse_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm device info\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');

    elif profileMode == 3:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("Full Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/caffe2nnir2openvx_fp16_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm device info\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');

    elif profileMode == 4:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("Full Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/onnx2nnir2openvx_noFuse_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm device info\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md'); 

    elif profileMode == 5:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("Full Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/onnx2nnir2openvx_fuse_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm device info\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md'); 

    elif profileMode == 6:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("Full Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/onnx2nnir2openvx_fp16_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm device info\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md'); 
    
    elif profileMode == 7:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("Full Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/nnef2nnir2openvx_noFuse_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm device info\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md'); 

    elif profileMode == 8:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("Full Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/nnef2nnir2openvx_fuse_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm device info\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md'); 

    elif profileMode == 9:
        print("\nGenerating Report File...\n")
        with open(report_filename, 'w') as f:

            f.write("Full Report\n")
            f.write("=====================\n")
            f.write("\n")
            f.write("Generated: %s\n" % report_dtstr)
            f.write("\n")
            f.write("\n\nBenchmark Report\n")
            f.write("--------\n")
            f.write("\n")
            with open(buildDir_MIVisionX+'/develop/nnef2nnir2openvx_fp16_profile.md') as benchmarkFile:
                for line in benchmarkFile:
                    f.write("%s" % line)

            f.write("\n")
            f.write("\n")

            f.write("\n\nPlatform Report\n")
            f.write("--------\n")
            f.write("\n")
            f.write("Platform: %s (%s)\n" % (platform_name_fq, platform_ip))
            f.write("\n")

            write_formatted(sys_info, f)
            write_formatted(cpu_info, f)
            write_formatted(gpu_info, f)
            write_formatted(board_info, f)
            write_formatted(memory_info, f)

            f.write("ROCm\n")
            f.write("-------------\n")
            f.write("\n")
            write_lines_as_table(['Package', 'Version'], rocm_packages, f)
            f.write("\n\n\n")

            f.write("Vbios\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(vbios, f)
            f.write("\n")
            f.write("ROCm device info\n")
            f.write("-------------\n")
            f.write("\n")
            write_formatted(rocmInfo, f)
            f.write("\n")

            f.write("Dynamic Libraries\n")
            f.write("-----------------\n")
            f.write("\n")
            write_formatted(lib_tree, f)
            f.write("\n")

            f.write("\n\n---\nCopyright AMD 2018\n")

        ## File diff generator
        diffFolder = '~/.AMDOVX-Diff'
        diffFolder_dir = os.path.expanduser(diffFolder)

        if(os.path.exists(diffFolder_dir)):
            print("\nGenerating Diff File...\n")
            titleName = 'Diff-Report'
            os.system('diff -y --suppress-common-lines '+report_filename+' '+diffFolder_dir+'/latestReportFile.md | aha --black --title '+titleName+' > reportDiff.html');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md');
        else:
            os.system('(cd ; mkdir '+diffFolder_dir+')');
            os.system(' cp '+report_filename+' '+diffFolder_dir+'/latestReportFile.md'); 
exit(0)
