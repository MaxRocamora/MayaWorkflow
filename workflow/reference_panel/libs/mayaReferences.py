# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# This Class handles references control in a maya scene
# You must create an object for each reference to use, use getReferences
# staticmethod to collect selected references as objects
# --------------------------------------------------------------------------------------------

import re
import os
import maya.cmds as cmds
import maya.mel as mel


class MayaReference():
    ''' Creates a maya reference object from node '''

    def __init__(self, _node=None):
        self._node = _node

    @staticmethod
    def getReferences(selected=False):
        ''' returns a list of maya references from
        scene selection in form of objects '''
        selected_references = []
        if selected:
            sel = cmds.ls(sl=True)
        else:
            sel = cmds.ls(type="reference")
        for item in sel:
            ref_node = cmds.referenceQuery(item, rfn=True)
            if ref_node not in selected_references:
                selected_references.append(ref_node)

        return [MayaReference(r) for r in selected_references]

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
    def namespace_number(tail_self):
        ''' Returns namespace ending numbers of this reference '''
        ns = self.namespace.split(":")[1]
        number = re.findall('\d+', ns)
        try:
            return str(number[0])
        except IndexError:
            return ''

    @property
    def maya_nodes(self):
        ''' Returns the maya nodes inside of this reference '''
        return cmds.referenceQuery(self.name, nodes=True)

    @property
    def ref_filepath(self):
        '''return the filepath of the reference file'''
        return cmds.referenceQuery(self.name, f=True)

    @property
    def ref_filepath_id(self):
        '''return numer id of the filepath for
        files referenced multiple times'''
        return self.ref_filepath.split('.ma')[1]

# --------------------------------------------------------------------------------------------
# METHODS
# --------------------------------------------------------------------------------------------

    def select(self):
        ''' Select the nodes of this reference '''
        cmds.select(self.maya_nodes, r=True)

    def reload(self):
        '''reload reference'''
        cmds.file(self.ref_filepath, loadReference=self.name)

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
        items = self.maya_nodes
        if items is not None:
            cmds.select(items[0], r=True)
            try:
                mel.eval('duplicateReference 0 ""')
            except RuntimeError:
                # print "Something fail at duplicating this reference"
                pass

    def replace_file_for(self, new_filename):
        ''' Replaces the file of a reference '''
        cmds.file(new_filename, loadReference=self.node)

    def auto_update_namespace(self):
        ''' set namespace to match reference file name and preserves id '''
        old_namespace = self.namespace.split(":")[1]
        path, filename = os.path.split(self.ref_filepath)
        filename, file_extension = os.path.splitext(filename)
        new_name = filename + '_' + self.namespace_tail_number
        if not cmds.namespace(exists=new_name):
            cmds.namespace(rename=(old_namespace, new_name))
