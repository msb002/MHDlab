# -*- coding: utf-8 -*-

import os

def create_tcdict(filepaths, loadfn, prefix = None ):
    """takes in a list of files and a lod function, and creates a dict of a df for each file. If a prefix is passed, that is removed from the filename (typically the instrument name so only the test case is left as the dict key)"""

    dfs = {}

    for filepath in filepaths:
        filename = os.path.split(filepath)[1]
        testcase = os.path.splitext(filename)[0]

        if prefix != None:
            testcase = _remove_prefix(testcase,prefix)

        df =  loadfn(filepath)
        dfs[testcase] =df
    
    return dfs


def _remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s