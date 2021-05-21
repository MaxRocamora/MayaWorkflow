# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
'''
TD Actions

'''

VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0

version = '{}.{}.{}'.format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
__version__ = version

__app__ = 'TD_Actions'
__qt__ = 'Arcane2:Qt_' + __app__ + '_ui'

__all__ = ['version', '__version__', '__app__', '__qt__']
