# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# Author: Maximiliano Rocamora
# Mini Panel for Maya Reference control
# import arcane.workflow.refPanel.main as refp; reload(refp)
# --------------------------------------------------------------------------------------------
from __future__ import print_function
import os

from PySide2 import QtGui, QtCore
import maya.cmds as cmds

from a2core.ui.css.window_styler import WindowsStyler
import maya_scr.utils.mayaNodeSelector as mayaNodeSelector
from maya_scr.utils.qt_loader_maya import load_ui, get_maya_main_window
from maya_scr.workflow.refPanel.version import *

path = os.path.dirname(__file__)
form, base = load_ui(os.path.join(path, 'ui', 'main_ui.ui'))


class ReferencePanel(base, form):
    def __init__(self, parent=get_maya_main_window()):
        super(ReferencePanel, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setObjectName(__qt__)
        self.css = WindowsStyler(self, __file__, 'RP')
        self.mns = mayaNodeSelector.mayaNodeSelector()
        self.setIcons()
        self.setConnections()
        self.offset = (self.pos())

# --------------------------------------------------------------------------------------------
# CONNECTIONS & BUTTONS
# --------------------------------------------------------------------------------------------

    def setIcons(self):
        reloadIcon = QtGui.QIcon(path + '/icons/refresh.png')
        selectIcon = QtGui.QIcon(path + '/icons/select.png')
        loadIcon = QtGui.QIcon(path + '/icons/load.png')
        unloadIcon = QtGui.QIcon(path + '/icons/unload.png')
        duplicateIcon = QtGui.QIcon(path + '/icons/duplicate.png')
        removeIcon = QtGui.QIcon(path + '/icons/remove.png')
        self.btn_reload.setIcon(reloadIcon)
        self.btn_select.setIcon(selectIcon)
        self.btn_load.setIcon(loadIcon)
        self.btn_unload.setIcon(unloadIcon)
        self.btn_duplicate.setIcon(duplicateIcon)
        self.btn_remove.setIcon(removeIcon)

    def setConnections(self):
        ''' Connections UI '''
        self.btn_reload.clicked.connect(self.reloadRef)
        self.btn_select.clicked.connect(self.selectRef)
        self.btn_load.clicked.connect(self.loadRef)
        self.btn_unload.clicked.connect(self.unloadRef)
        self.btn_duplicate.clicked.connect(self.duplicateRef)
        self.btn_remove.clicked.connect(self.removeRef)
        self.mnu_replaceFiles.triggered.connect(self.repath)
        self.mnu_updateReferenceNs.triggered.connect(self.restoreRefName)

# --------------------------------------------------------------------------------------------
# QUICK BUTTONS ACTIONS
# --------------------------------------------------------------------------------------------

    def reloadRef(self):
        for item in self.mns.getReferencesObject(selected=True):
            item.reload()

    def unloadRef(self):
        for item in self.mns.getReferencesObject(selected=True):
            item.unload()

    def loadRef(self):
        for item in self.mns.getReferencesObject(selected=True):
            item.load()

    def removeRef(self):
        for item in self.mns.getReferencesObject(selected=True):
            item.remove()

    def duplicateRef(self):
        for item in self.mns.getReferencesObject(selected=True):
            item.duplicate()

    def selectRef(self):
        for item in self.mns.getReferencesObject(selected=True):
            item.select()

# --------------------------------------------------------------------------------------------
# MENU BAR ACTIONS
# --------------------------------------------------------------------------------------------

    def restoreRefName(self):
        for item in self.mns.getReferencesObject(selected=True):
            item.updateNamespace()

    def repath(self):
        if self.browseFilePath():
            for item in self.mns.getReferencesObject(selected=True):
                item.replaceFile(self.newFile)

    def browseFilePath(self):
        ''' Open folder for file search '''
        userPath = cmds.fileDialog2(dialogStyle=1, fm=1)
        if userPath:
            self.newFile = userPath[0]
            if "\\" in self.newFile:
                self.newFile = self.newFile.replace("\\", "/")
            return True
        else:
            return False

# --------------------------------------------------------------------------------------------
# DRAG UI
# --------------------------------------------------------------------------------------------

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)


def main():
    if cmds.window(__qt__, q=1, ex=1):
        cmds.deleteUI(__qt__)
    app = ReferencePanel()
    app.show()


main()  # tools published with reload
