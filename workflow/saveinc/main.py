# -*- coding: utf-8 -*-
from __future__ import print_function

import maya.mel as mel
import maya.cmds as cmds


def save_incremental():
    ''' saves maya incremental '''
    print("Saving Incremental")
    cmds.file(modified=True)
    mel.eval("incrementAndSaveScene 0;")
