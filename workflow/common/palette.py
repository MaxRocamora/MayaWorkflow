from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QStyleFactory


# Colors

# Main Background
QC_Main = QColor(55, 55, 55)
QC_Text = QColor(127, 127, 127)
QC_Base = QColor(42, 42, 42)
QC_AlterBase = QColor(66, 66, 66)
QC_DisabledHl = QColor(80, 80, 80)
QC_Shadow = QColor(20, 20, 20)
QC_Link = QColor(42, 130, 218)
QC_Highlight = QColor(42, 130, 218)
QC_Dark = QColor(35, 35, 35)


def dark_palette(app):
    darkPalette = app.palette()
    darkPalette.setColor(QPalette.Window, QC_Main)
    darkPalette.setColor(QPalette.WindowText, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QC_Text)
    darkPalette.setColor(QPalette.Base, QC_Base)
    darkPalette.setColor(QPalette.AlternateBase, QC_AlterBase)
    darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
    darkPalette.setColor(QPalette.ToolTipText, Qt.white)
    darkPalette.setColor(QPalette.Text, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.Text, QC_Text)
    darkPalette.setColor(QPalette.Dark, QC_Dark)
    darkPalette.setColor(QPalette.Shadow, QC_Shadow)
    darkPalette.setColor(QPalette.Button, QC_Main)
    darkPalette.setColor(QPalette.ButtonText, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QC_Text)
    darkPalette.setColor(QPalette.BrightText, Qt.red)
    darkPalette.setColor(QPalette.Link, QC_Link)
    darkPalette.setColor(QPalette.Highlight, QC_Highlight)
    darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QC_DisabledHl)
    darkPalette.setColor(QPalette.HighlightedText, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QC_Text)
    app.setPalette(darkPalette)
    app.setStyle(QStyleFactory.create('Fusion'))
    # print(QStyleFactory.keys())
