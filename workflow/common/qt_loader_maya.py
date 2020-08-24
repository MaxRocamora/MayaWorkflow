# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
from cStringIO import StringIO
import xml.etree.ElementTree as xml
from PySide2 import QtWidgets
import pyside2uic as pysideuic
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def load_ui(uiFile):
    """ :author: Jason Parks
    Pyside lacks the "loadUiType" command, so we have to convert
    the ui file to py code in-memory first
    and then execute it in a special frame
    to retrieve the form_class. """
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their
        # type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtWidgets, widget_class)
    return form_class, base_class
