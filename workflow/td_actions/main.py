# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# TD Actions
# A dinamic interface that creates a dropdown list with each method found in actions libs
#
# Author: Maximiliano Rocamora / maxirocamora@gmail.com
# https://github.com/MaxRocamora/Workflow
# --------------------------------------------------------------------------------------------
from inspect import getmembers, isfunction

import maya.cmds as cmds

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QSize, QRect

from workflow.common.window_styler import WindowsStyler
from workflow.common.qt_loader_maya import get_maya_main_window
import workflow.td_actions.libs.actions as actions
from workflow.td_actions.version import __qt__, __app__


class TDActions(QtWidgets.QMainWindow):
    def __init__(self, parent=get_maya_main_window(), **kwargs):
        super(TDActions, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowModality(Qt.NonModal)
        self.setWindowFlags(Qt.Tool)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.css = WindowsStyler(self, __file__)
        self._setupUi()
        self.reset_ui()

    def _setupUi(self):
        ''' initializes ui '''
        # window / layout / centralwidget / frame
        self.setObjectName(__qt__)
        self.setWindowTitle(__app__)
        self.setFixedSize(300, 150)
        fixed = QtWidgets.QSizePolicy.Fixed
        sizePolicy = QtWidgets.QSizePolicy(fixed, fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # centralwidget / layout
        self.central = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setObjectName("verticalLayout")
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)
        # frame
        self.frame = QtWidgets.QFrame()
        self.frame.setObjectName("frame")
        self.layout.addWidget(self.frame)

        # groupbox
        self.group_box = QtWidgets.QGroupBox(self.frame)
        self.group_box.setObjectName("group_box")
        self.group_box.setGeometry(QRect(5, 5, 290, 140))
        self.group_box.setStyleSheet('background: rgb(60, 60, 60)')

        # combobox
        self.cbox_methods = QtWidgets.QComboBox(self.group_box)
        self.cbox_methods.setObjectName("projects")
        size = QSize(288, 25)
        self.cbox_methods.setSizePolicy(sizePolicy)
        self.cbox_methods.setMinimumSize(size)
        self.cbox_methods.setMaximumSize(size)
        self.cbox_methods.setParent(self)
        self.cbox_methods.move(6, 25)

        # button
        self.btn_set = QtWidgets.QPushButton(self.group_box)
        self.btn_set.setGeometry(QRect(0, 0, 121, 31))
        self.btn_set.setObjectName("button")
        self.btn_set.setText('RUN COMMAND')
        self.btn_set.move(90, 70)
        self.css.css_button(self.btn_set, color='blue')
        self.btn_set.clicked.connect(self.run_command)
        
        # statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)

        self.show()

    def reset_ui(self):
        ''' fill combobox with methods and store them in self.method '''
        self.methods = [o for o in getmembers(actions) if isfunction(o[1])]
        self.cbox_methods.clear()
        for name in self.methods:
            self.cbox_methods.addItem(name[0])

# -------------------------------------------------------------------------------------------
# MAIN UI METHODS
# --------------------------------------------------------------------------------------------

    def run_command(self):
        ''' run selected command '''
        method = self.methods[self.cbox_methods.currentIndex()]
        self.display_message('Running: %s', method[0], 1)
        msg, status = method[1]()
        self.display_message(msg, status)

# --------------------------------------------------------------------------------------------
# UTILITY METHODS
# --------------------------------------------------------------------------------------------

    def display_message(self, message, status, timed=0):
        ''' display given message over given time'''
        if status:
            color = 'lime'
        else:
            color = 'orange'

        css = "color: {}; background: {};".format(
            color, 'rgb(20, 20, 20)')
        self.statusbar.setStyleSheet(css)
        if timed > 0:
            self.statusbar.showMessage(message, timed)
        else:
            self.statusbar.showMessage(message)

# --------------------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------------------


def load():
    if cmds.window(__qt__, q=1, ex=1):
        cmds.deleteUI(__qt__)
    app = TDActions()
    app.show()
