# -*- coding: utf-8 -*-
"""
Add repository to the pythonpath
"""
import os
import sys
import site

# #Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
# PythonAnalysisPath = os.getcwd()
# if not PythonAnalysisPath in sys.path:
#     sys.path.append(PythonAnalysisPath)


sitepath = site.getsitepackages()[1]
filepath = os.path.join(sitepath,'MHDpath.pth')
MHDdir = os.getcwd()

with open(filepath,'w') as write_file:
    write_file.write(MHDdir)

print('added',MHDdir,'to as .pth file in ',sitepath)