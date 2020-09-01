# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# 3dsmax style renamer (2015)
# Author: Maximiliano Rocamora / maxirocamora@gmail.com
# https://github.com/MaxRocamora/Workflow
# --------------------------------------------------------------------------------------------
from __future__ import print_function
import os

import maya.cmds as cmds

from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from workflow.common.window_styler import WindowsStyler
from workflow.common.qt_loader_maya import load_ui, get_maya_main_window
from workflow.renamer.version import *

ui_path = os.path.dirname(__file__)
form, base = load_ui(os.path.join(ui_path, 'ui', 'main_ui.ui'))


def undo(func):
    ''' maya undo decorator '''
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
        return ret
    return wrapper


class Renamer(base, form):
    def __init__(self, parent=get_maya_main_window()):
        super(Renamer, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(Qt.Tool)
        self.setupUi(self)
        self.setObjectName(__qt__)
        self.css = WindowsStyler(self, __file__)
        self.set_connections()
        self.reset_ui()

# -------------------------------------------------------------------------------------------
# CONNECTIONS & INIT METHODS
# --------------------------------------------------------------------------------------------

    def set_connections(self):
        ''' Connections '''
        self.css.css_button(self.btn_rename, 'blue')
        self.btn_rename.clicked.connect(self.rename_pressed)
        self.css.css_button(self.btn_replace, 'blue')
        self.btn_replace.clicked.connect(self.replace)

    def reset_ui(self):
        ''' Reset Variables and UI widgets '''
        self.rad_selection.setChecked(True)
        self.input_suffix = ""
        self.input_prefix = ""
        self.rem_prefix = 0
        self.rem_last = 0
        self.input_basename = ""
        self._basenumber = 1
        self._step = 1
        self._padding = 4

# -------------------------------------------------------------------------------------------
# MAIN UI & MENUBAR METHODS
# --------------------------------------------------------------------------------------------

    def read_ui(self):
        ''' Reads the UI user data '''

        # Read UI and set vars.

        # autounderscore
        if self.mnu_underscore.isChecked():
            self.underscore = '_'
        else:
            self.underscore = ''

        self.input_prefix = self.line_prefix.text()
        self.input_suffix = self.line_suffix.text()
        self.input_basename = self.line_name.text()

        # Removes Digit UI
        if self.is_number(self.line_removefirst.text()):
            self.rem_prefix = int(self.line_removefirst.text())
        else:
            self.rem_prefix = 0

        if self.is_number(self.line_removelast.text()):
            self.rem_last = int(self.line_removelast.text())
        else:
            self.rem_last = 0

        # Serial padding UI
        if self.is_number(self.line_basenumber.text()):
            self._basenumber = int(self.line_basenumber.text())
            if self._basenumber > 100000:
                self._basenumber = 100000
                self.line_basenumber.setText("100000")
        else:
            self._basenumber = 0

        if self.is_number(self.line_step.text()):
            self._step = int(self.line_step.text())
            if self._step > 1000:
                self._step = 1000
                self.line_step.setText("1000")
        else:
            self._step = 0

        if self.is_number(self.line_padding.text()):
            self._padding = int(self.line_padding.text())
            if self._padding > 10:
                self._padding = 10
                self.line_padding.setText("10")
        else:
            self._padding = 0

# --------------------------------------------------------------------------------------------
# RENAME METHODS
# --------------------------------------------------------------------------------------------

    @undo
    def rename_pressed(self):
        ''' rename button callback '''
        self.read_ui()
        ud = self.underscore
        rem_first_checked = self.chk_removefirst.isChecked()
        rem_last_checked = self.chk_removelast.isChecked()

        # take selection
        ui_selection = cmds.ls(sl=True, uuid=True)
        if len(ui_selection) < 1:
            return

        for item in ui_selection:
            obj = cmds.ls(item)
            __name = str(obj[0])

            # remove first digits if you are not setting a base name
            if rem_first_checked and not self.chk_name.isChecked():
                if self.rem_prefix < (len(__name)) and self.rem_prefix > 0:
                    __name = __name[self.rem_prefix:]

            # remove last digit if you are not setting a base name
            if rem_last_checked and not self.chk_name.isChecked():
                if self.rem_last < (len(__name)) and self.rem_last > 0:
                    __name = __name[0:-self.rem_last]

            # base rename
            if self.chk_name.isChecked():
                if not self.input_basename:
                    self.alert(
                        "Enter a basename or disable checkbox!", "Ops!")
                    return False
                else:
                    if self.is_number(self.input_basename):
                        self.alert(
                            "Your basename must not contain numbers",
                            "Ops!"
                        )
                        return False
                    else:
                        __name = self.input_basename

            # add prefix
            if self.chk_prefix.isChecked():
                if not self.input_prefix:
                    self.alert(
                        "Enter a prefix or disable checkbox!", "Ops!")
                    return False
                else:
                    if self.is_number(self.input_prefix):
                        self.alert(
                            "Your prefix name cannot be a number", "Ops!")
                        return False
                    else:
                        __name = self.input_prefix + ud + __name

            # add suffix
            if self.chk_suffix.isChecked():
                if not self.input_suffix:
                    self.alert(
                        "Enter a suffix or disable checkbox!", "Ops!")
                    return False
                else:
                    __name = __name + ud + self.input_suffix

            # add serializing and padding
            if self.chk_number.isChecked():
                padholder = str(self._basenumber)
                padholder = padholder.zfill(self._padding)
                __name = __name + "_" + padholder

            # rename it!
            if self.is_number(__name):
                print("skipping this item, the result is a number: ", obj)
            else:
                cmds.rename(obj, __name)

            self._basenumber += self._step

# --------------------------------------------------------------------------------------------
# Replace Methods
# --------------------------------------------------------------------------------------------

    def replace(self):
        replace_text = str(self.line_find.text())
        with_text = str(self.line_replace.text())

        if self.rad_scene.isChecked():
            nodes = cmds.ls()
        else:
            nodes = cmds.ls(sl=True)

        self.find_replace(nodes, replace_text, with_text)

    @undo
    def find_replace(self, nodes, find_text, replace_text):
        ''' Find and replaces text, get nodes are based
        on scene or maya seletion '''
        shapes = cmds.ls(nodes, s=True)
        shape_set = set(shapes)

        new_nodes_names = []
        failed_nodes = []
        for node in nodes:
            if find_text not in node:
                continue
            if node in shape_set:
                continue

            try:
                new_nodes_names.append((node, cmds.rename(node, '__tmp__')))
            except RuntimeError:
                failed_nodes.append(node)

        for shape in shapes:
            if find_text not in shape:
                continue
            if not cmds.objExists(shape):
                try:
                    new_name = cmds.rename(
                        shape, shape.replace(find_text, '__tmp__'))
                    new_nodes_names.append((shape, new_name))
                except RuntimeError:
                    failed_nodes.append(node)

        new_names = []
        for name, new_node in new_nodes_names:
            new_name = name.replace(find_text, replace_text)
            new_names.append(cmds.rename(new_node, new_name))

        return new_names

# --------------------------------------------------------------------------------------------
# UTILITY METHODS
# --------------------------------------------------------------------------------------------

    def is_number(self, s):
        """ check if a string is a number """
        try:
            int(s)
            return True
        except ValueError:
            return False

    def alert(self, msg, title):
        """ Opens a messagebox UI
            msg: string.
            title: string.
        """
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.exec_()

# --------------------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------------------


def load():
    if cmds.window(__qt__, q=1, ex=1):
        cmds.deleteUI(__qt__)
    app = Renamer()
    app.show()
