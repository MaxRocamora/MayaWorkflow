# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# MAYA UTILS
# This lib hold maya scene methods for common fixes or procedures
# All method should return a tuple ('message', 'sucess_status') [str, bool]
# --------------------------------------------------------------------------------------------
import maya.mel as mel
import maya.cmds as cmds
import re

# --------------------------------------------------------------------------------------------
# MAYA SCENE
# --------------------------------------------------------------------------------------------

def remove_unknown_plugins():
    ''' removes missing plugins from ma file '''
    if cmds.unknownPlugin(query=1, list=1):
        for plug in cmds.unknownPlugin(query=1, list=1):
            try:
                cmds.unknownPlugin(plug, remove=1)
            except RuntimeError as e:
                return 'Error Removing {}'.format(plug) + '\n' + str(e), 0
    return 'Unknown Plugins removed', 1


def unlock_for_delete_orthographic_cameras():
    ''' unlock orthographic camera so it can be deleted '''
    sel = cmds.ls(sl=True)
    if not len(sel):
        return 'Select cameras first!', 0

    for cam in sel:
        try:
            cmds.camera(cam, e=True, startupCamera=False)
        except RuntimeError:
            pass
        
    return ("Selected orthographic cameras can be deleted now."), 1


def restore_render_UI():
    ''' removes and restore render ui window '''
    try:
        mel.eval("deleteUI unifiedRenderGlobalsWindow")
        mel.eval("buildNewSceneUI")
        status = 1
    except RuntimeError:
        status = 0
    return 'Script executed!', status


def kill_turtle_plugin():
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
        msg, status = 'Unable to unload Turtle', 0
    
    msg, status = 'Turtle Killed', 1
    return msg, status


def cleanup_DCF_updateViewportList():
    ''' removes from uiConfigurationScriptNode and scene the nasty
    bug message from DCF_updateViewportList '''
    msg, status = 'DCF_updateViewportList ScriptNode Not Found', 0
    if cmds.objExists("uiConfigurationScriptNode"):
        bs = cmds.scriptNode('uiConfigurationScriptNode', q=True, bs=True)
        if bs:
            msg, status = 'DCF_updateViewportList Removed', 1
            bs = re.sub(r'DCF_updateViewportList;', bs, '')
        cmds.scriptNode('uiConfigurationScriptNode', e=True, bs=bs)
    return msg, status

# --------------------------------------------------------------------------------------------
# MAYA ATTRIBUTES
# --------------------------------------------------------------------------------------------


def unlock_basic_channels():
    ''' unlocks and restore channels '''
    basic_attributes = ['.tx', '.ty', '.tz',
                        '.rx', '.ry', '.rz',
                        '.sx', '.sy', '.sz',
                        '.v']
    sel = cmds.ls(sl=True)
    if not sel:
        return 'Nothing Selected!', False

    meshes = cmds.listRelatives(sel, pa=True, type="mesh")
    all_shapes = cmds.listRelatives(meshes, parent=True, fullPath=False)
    if all_shapes is None:
        return 'No shape found on selection', 0

    if len(all_shapes) <=0:
        return "No meshes selected to unlock_channels.", 0

    for each in all_shapes:
        for at in basic_attributes:
            cmds.setAttr(each + at, lock=False, channelBox=True)
            cmds.setAttr(each + at, k=True)
        
    msg = "Channels unlocked on ({}) transform nodes".format(len(all_shapes))
    return msg, 1


def unlock_all_channels():
    ''' unlocks and restore all maya channels '''
    sel = cmds.ls(sl=True)
    mesh = cmds.listRelatives(sel, pa=True, type="mesh")  # filter shapes (meshes)
    # get transforms names of the shapes
    all_mesh = cmds.listRelatives(mesh, parent=True, fullPath=False)
    if all_mesh is not None:
        count = len(all_mesh)
    else:
        count = 0
    mesh_count = 0  # channel count
    user_att_count = 0
    if count > 0:  # 1 o varios items
        for each in all_mesh:
            mesh_count += 1
            at_list = cmds.listAttr(each)
            for at in at_list:
                obj = each + "." + at.split('.')[-1]
                if cmds.objExists(obj):
                    user_att_count += 1
                    cmds.setAttr(obj, lock=False)
        msg = "({}) Channels unlocked on ({}) transform nodes".format(
            user_att_count, mesh_count)
        status = 1
    else:
        msg, status = "Select Meshes to unlock all channels first.", 0
    return msg, status


def delete_custom_attributes():
    ''' delete all custom attributes '''
    rawSel = cmds.ls(sl=True)  # raw selection
    rawMesh = cmds.listRelatives(
        rawSel, pa=True, type="mesh")  # filter shapes (meshes)
    # get transforms names of the shapes
    allSel = cmds.listRelatives(rawMesh, parent=True, fullPath=False)
    if not allSel == None:
        count = len(allSel)
    else:
        count = 0
    mesh_count = 0  # channel count
    user_att_count = 0
    mesh_count = 0
    if count > 0:  # 1 o varios items
        for each in allSel:
            mesh_count += 1
            at_list = cmds.listAttr(each, ud=True)
            if at_list > 0:
                for at in at_list:
                    user_att_count += 1
                    attribute = each + "." + at
                    if cmds.objExists(attribute):
                        cmds.setAttr(attribute, l=False)
                        cmds.deleteAttr(attribute)
        msg = "({}) custom attributes deleted over ({}) transform nodes".format(
            user_att_count, mesh_count)
        alert = False
    else:
        msg, alert = "Select Meshes to delete custom attributes first.", True
    return msg, alert

# --------------------------------------------------------------------------------------------
# MAYA MESH CORE METHODS
# Operations on meshes
#
# delete history
# freeze transformations
# centerPivot
# clean Combine
# clean Separate
# clean duplicate
# copy Pivot
# restore shapes names
# --------------------------------------------------------------------------------------------
