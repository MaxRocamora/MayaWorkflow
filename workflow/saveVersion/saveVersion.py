# -*- coding: utf-8 -*-
import maya.mel as mel
import maya.cmds as cmds


def saveIncremental():
    # saves maya in a new version by force
    print "Saving Incremental"
    cmds.file(modified=True)
    mel.eval("incrementAndSaveScene 0;")
