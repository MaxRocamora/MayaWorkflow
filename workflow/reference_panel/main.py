# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# Author: Maximiliano Rocamora
# Maya References Picker from viewport
# import arcane.workflow.refPanel.main as refp; reload(refp)
# --------------------------------------------------------------------------------------------
import os

from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QApplication

import maya.cmds as cmds
import pymel as pm

from workflow.common.qt_loader_maya import load_ui, get_maya_main_window
import workflow.reference_panel.libs.mayaReferences as MayaRef
from .version import *
from . import *

path = os.path.dirname(__file__)
form, base = load_ui(os.path.join(path, 'ui', 'main_ui.ui'))


class ReferencePanel(base, form):
    def __init__(self, parent=get_maya_main_window()):
        super(ReferencePanel, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setObjectName(__qt__)
        self.config_ui()
        self.maya_references = MayaRef.MayaReference()

        self.move(
            QApplication.desktop().screen().rect().center() - self.rect().center()
        )

        self.drag_position = 0
        self.draggin = False

    def config_ui(self):
        # general css
        self.top_frame.setStyleSheet("""
            QFrame {
                    background-color: rgba(35, 35, 35, 255);
            }
            """)
        self.lbl_title.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.ui_frame.setStyleSheet("""
            QFrame {
                    background-color: rgba(50, 50, 50, 255);
            }
            """)

        self.btn_select.setStyleSheet(css_select)
        self.btn_reload.setStyleSheet(css_reload)
        self.btn_load.setStyleSheet(css_load)
        self.btn_unload.setStyleSheet(css_unload)
        self.btn_remove.setStyleSheet(css_remove)
        self.btn_duplicate.setStyleSheet(css_duplicate)
        self.btn_filepath.setStyleSheet(css_replace)
        self.btn_namespace.setStyleSheet(css_namespace)

        # icons
        self.btn_close.setIcon(QtGui.QIcon(path + '/icons/close.png'))

        # connections
        self.btn_close.clicked.connect(lambda: self.close())
        self.btn_select.clicked.connect(lambda: self.ref_callback('select'))
        self.btn_reload.clicked.connect(lambda: self.ref_callback('reload'))
        self.btn_load.clicked.connect(lambda: self.ref_callback('load'))
        self.btn_unload.clicked.connect(lambda: self.ref_callback('unload'))
        self.btn_duplicate.clicked.connect(lambda: self.ref_callback('duplicate'))
        self.btn_remove.clicked.connect(lambda: self.ref_callback('remove'))
        self.btn_namespace.clicked.connect(lambda: self.ref_callback('auto_update_namespace'))
        self.btn_filepath.clicked.connect(self.repath)

    # --------------------------------------------------------------------------------------------
    # BUTTONS ACTIONS
    # --------------------------------------------------------------------------------------------

    def ref_callback(self, action):
        for item in self.selected_ui_references(selected=True):
            method = getattr(item, action)
            method()

    def repath(self):
        new_file = self.browse_file()
        if new_file:
            for item in self.selected_ui_references(selected=True):
                item.replace_file_for(new_file)

    def browse_file(self):
        ''' Open folder for file search, returns selected file '''
        file_selected = cmds.fileDialog2(dialogStyle=1, fm=1)
        if file_selected:
            return file_selected[0].replace(os.sep, "/")
        return False

    # --------------------------------------------------------------------------------------------
    # REFERENCE OBJECTS
    # --------------------------------------------------------------------------------------------

    def selected_ui_references(self, selected=False):
        ''' Get reference object list from selection.
        Args:
            selected (boolean) if true get objects from maya selection.
        Returns:
            list of reference objects
        '''
        if selected:
            return self.maya_references.getReferences(selected=True)
        else:
            # get references from scene (pymel)
            return pm.core.listReferences(parentReference=None,
                                          recursive=False,
                                          namespaces=False,
                                          refNodes=True,
                                          references=False)

    # --------------------------------------------------------------------------------------------
    # DRAG UI
    # --------------------------------------------------------------------------------------------

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.draggin:
            self.move(self.pos() + event.globalPos() - self.drag_position)
            self.drag_position = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.draggin = False

    def mousePressEvent(self, event):
        self.draggin = True
        self.drag_position = event.globalPos()


def load():
    if cmds.window(__qt__, q=1, ex=1):
        cmds.deleteUI(__qt__)
    app = ReferencePanel()
    app.show()
