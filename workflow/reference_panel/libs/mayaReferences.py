# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# This Class handles references control in a maya scene
# You must create an object for each reference to use.
'''
import mayaReferences

refInSelection = []
sel = cmds.ls(sl=True)
for item in sel:
    thisRef = cmds.referenceQuery(item, rfn=True)
    if thisRef not in refInSelection:
        refInSelection.append(thisRef)

return [mayaReferences.mayaReference("none", r) for r in refInSelection]
'''
# --------------------------------------------------------------------------------------------

import re
import os
import maya.cmds as cmds
import maya.mel as mel


class MayaReference():
    ''' Creates a maya reference object from node '''

    def __init__(self, _node=None):
        self._node = _node

    def __str__(self):
        return "Maya Single Reference Object Class"

    @staticmethod
    def getReferences(selected=False):
        ''' Returs list of maya references from
        scene selection in form of objects '''
        refInSelection = []
        if selected:
            sel = cmds.ls(sl=True)
        else:
            sel = cmds.ls(type="reference")
        for item in sel:
            thisRef = cmds.referenceQuery(item, rfn=True)
            if thisRef not in refInSelection:
                refInSelection.append(thisRef)

        return [MayaReference(r) for r in refInSelection]

# --------------------------------------------------------------------------------------------
# PROPERTIES
# --------------------------------------------------------------------------------------------

    @property
    def name(self):
        ''' Returns string type name of this reference '''
        return str(self.node)

    @property
    def node(self):
        ''' Returns maya node name of this reference '''
        return self._node

    @property
    def namespace(self):
        ''' Returns namespace of this reference '''
        return cmds.referenceQuery(str(self.node), namespace=True)

    @property
    def namespaceNumber(self):
        ''' Returns namespace ending numbers of this reference '''
        ns = self.namespace.split(":")[1]
        number = re.findall('\d+', ns)
        try:
            return str(number[0])
        except IndexError:
            return ''

    @property
    def mayaNodes(self):
        ''' Returns the maya nodes inside of this reference '''
        return cmds.referenceQuery(self.name, nodes=True)

    @property
    def rFile(self):
        '''return the filepath of the reference file'''
        return cmds.referenceQuery(self.name, f=True)

    @property
    def rFileId(self):
        '''return numer id of the filepath for
        files referenced multiple times'''
        return self.rFile.split('.ma')[1]

# --------------------------------------------------------------------------------------------
# METHODS
# --------------------------------------------------------------------------------------------

    def select(self):
        ''' Select the nodes of this reference '''
        cmds.select(self.mayaNodes, r=True)

    def reload(self):
        '''reload reference'''
        cmds.file(self.rFile, loadReference=self.name)

    def unload(self):
        ''' Unloads this reference '''
        cmds.file(unloadReference=self.node)

    def load(self):
        ''' Enables (load) this reference '''
        cmds.file(loadReferenceDepth="all", loadReference=self.node)

    def remove(self):
        ''' Removes this reference '''
        cmds.file(referenceNode=self.node, removeReference=True)

    def duplicate(self):
        ''' Duplicate this reference '''
        items = self.mayaNodes
        if items is not None:
            cmds.select(items[0], r=True)
            try:
                mel.eval('duplicateReference 0 ""')
            except RuntimeError:
                # print "Something fail at duplicating this reference"
                pass

    def replaceFile(self, newFile):
        ''' Replaces the file of a reference '''
        cmds.file(newFile, loadReference=self.node)

    def updateNamespace(self):
        ''' Set namespace to match reference file name and preserves id '''
        oldNs = self.namespace.split(":")[1]
        path, filename = os.path.split(self.rFile)
        filename, file_extension = os.path.splitext(filename)
        newName = filename + '_' + self.namespaceNumber
        if not cmds.namespace(exists=newName):
            cmds.namespace(rename=(oldNs, newName))
