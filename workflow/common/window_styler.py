# -*- coding: utf-8 -*-
''' Styles qt ui widgets '''
import os
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsDropShadowEffect


class WindowsStyler():
    def __init__(self, qtwindow, file, title=None):
        '''
        args:
            qtwindow (qt window widget)
            file (python __file__ of source app)
            title (str) predefined window title
        '''
        self.qtwindow = qtwindow
        self.path = os.path.dirname(file)

        # window title bar
        if title:
            qtwindow.setWindowTitle(title)

        self._load_css(qtwindow, self.path, title)

    @property
    def qss_file(self):
        qss = os.path.join(os.path.dirname(__file__), 'arcane2.qss')
        return qss

    def _load_css(self, qtwindow, path, title):
        ''' loads a qt css file into this qtwindows '''
        if not os.path.exists(self.qss_file):
            return

        with open(self.qss_file, "r") as fh:
            self.qtwindow.setStyleSheet(fh.read())

    def css_button(self, button, color=None, shadow=True):
        ''' apply arcane style to a button widget '''

        # default bg color is gray 80
        if color == 'red':
            bg_color = 'rgb(160, 20, 20)'  # red/white
            tx_color = 'rgb(255, 255, 255)'
        elif color == 'disabled':
            bg_color = 'rgb(80, 80, 80)'  # gray/gray
            tx_color = 'rgb(180, 180, 180)'
        elif color == 'blue':
            bg_color = 'rgb(46, 134, 193)'  # blue arcane/white
            tx_color = 'rgb(230, 230, 230)'
        else:
            bg_color = 'rgb(80, 80, 80)'  # gray
            tx_color = 'rgb(230, 230, 230)'

        css = "color:{};background:{};font-size:12px;font-family:Segoe UI;".format(tx_color, bg_color)
        button.setStyleSheet(css)

        if shadow:
            shadow = QGraphicsDropShadowEffect(self.qtwindow)
            shadow.setBlurRadius(6)
            shadow.setOffset(4)
            shadow.setColor(QColor(20, 20, 20, 200))
            button.setGraphicsEffect(shadow)
