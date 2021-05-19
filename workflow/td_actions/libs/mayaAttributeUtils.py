# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# MAYA ATTRIBUTE CORE METHODS
# Class Name Instance: attCore
##
# --------------------------------------------------------------------------------------------

import maya.cmds as cmds


class mayaAttributeCoreClass():

    def __init__(self, _name="maya attributes Core module"):
        self._name = _name

    def unlockBasicChannels(self):
        '''
        #unlocks and restore channels
        '''
        attlist = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']
        rawSel = cmds.ls(sl=True)  # raw selection
        rawMesh = cmds.listRelatives(rawSel, pa=True, type="mesh")  # filter shapes (meshes)
        # get transforms names of the shapes
        allSel = cmds.listRelatives(rawMesh, parent=True, fullPath=False)
        if allSel is not None:
            count = len(allSel)
        else:
            count = 0
        mcount = 0
        if count > 0:  # 1 o varios items
            for each in allSel:
                mcount += 1
                for at in attlist:
                    obj = each + at
                    cmds.setAttr(obj, lock=False, channelBox=True)
                    cmds.setAttr(obj, k=True)
            msg = "Channels unlocked on ({}) transform nodes".format(mcount)
            alert = False
        else:
            msg, alert = "Select Meshes to unlock_channels first.", True
        return msg, alert

    def unlockAllChannels(self):
        '''
        #unlocks and restore all maya channels
        '''
        rawSel = cmds.ls(sl=True)  # raw selection
        rawMesh = cmds.listRelatives(rawSel, pa=True, type="mesh")  # filter shapes (meshes)
        # get transforms names of the shapes
        allSel = cmds.listRelatives(rawMesh, parent=True, fullPath=False)
        if allSel is not None:
            count = len(allSel)
        else:
            count = 0
        mesh_count = 0  # channel count
        user_att_count = 0
        if count > 0:  # 1 o varios items
            for each in allSel:
                mesh_count += 1
                at_list = cmds.listAttr(each)
                for at in at_list:
                    at = at.split('.')[-1]
                    obj = each + "." + at
                    if cmds.objExists(obj):
                        user_att_count += 1
                        cmds.setAttr(obj, lock=False)
            msg = "({}) Channels unlocked on ({}) transform nodes".format(user_att_count, mesh_count)
            alert = False
        else:
            msg, alert = "Select Meshes to unlock_ALL_channels first.", True
        return msg, alert

    def deleteCustomAttributes(self):
        '''
        #delete all custom attributes
        '''
        rawSel = cmds.ls(sl=True)  # raw selection
        rawMesh = cmds.listRelatives(rawSel, pa=True, type="mesh")  # filter shapes (meshes)
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
