# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# MAYA SCENE LIB
# This lib hold maya scene methods for common fixes or procedures
# --------------------------------------------------------------------------------------------
from __future__ import print_function
import maya.mel as mel
import maya.cmds as cmds
import re


def removeUnknownPlugins():
    ''' removes missing plugins from ma file '''
    import maya.cmds as cmds
    if cmds.unknownPlugin(query=1, list=1):
        for plug in cmds.unknownPlugin(query=1, list=1):
            print('Removing Unknown Plugin:', plug)
            try:
                cmds.unknownPlugin(plug, remove=1)
            except RuntimeError as e:
                print('Error Removing {}'.format(plug) + '\n' + str(e))


def delOrthographicCameras():
    ''' unlock orthographic camera so it can be deleted '''
    sel = cmds.ls(sl=True)
    if len(sel) >= 1:
        for cam in sel:
            cmds.camera(cam, e=True, startupCamera=False)
            print("Selected orthographic cameras can be deleted now.")


def restoreRenderUi(self):
    ''' removes and restore render ui window '''
    try:
        mel.eval("deleteUI unifiedRenderGlobalsWindow")
        mel.eval("buildNewSceneUI")
    except RuntimeError:
        pass


def killTurtle():
    ''' removes turtle maya plugin from scene '''
    import pymel.core as pm
    try:
        pm.lockNode('TurtleDefaultBakeLayer', lock=False)
        pm.delete('TurtleDefaultBakeLayer')
    except:
        pass
    try:
        pm.lockNode('TurtleBakeLayerManager', lock=False)
        pm.delete('TurtleBakeLayerManager')
    except:
        pass
    try:
        pm.lockNode('TurtleRenderOptions', lock=False)
        pm.delete('TurtleRenderOptions')
    except:
        pass
    try:
        pm.lockNode('TurtleUIOptions', lock=False)
        pm.delete('TurtleUIOptions')
    except:
        pass
    try:
        pm.unloadPlugin("Turtle.mll")
    except ValueError:
        print('Cant unload Turtle')


def cleanup_DCF_updateViewportList():
    ''' removes from uiConfigurationScriptNode and scene the nasty
    bug message from DCF_updateViewportList '''
    if cmds.objExists("uiConfigurationScriptNode"):
        bs = cmds.scriptNode('uiConfigurationScriptNode', q=True, bs=True)
        if bs:
            print('Removing DCF_updateViewportList')
            bs = re.sub(r'DCF_updateViewportList;', bs, '')
        cmds.scriptNode('uiConfigurationScriptNode', e=True, bs=bs)
