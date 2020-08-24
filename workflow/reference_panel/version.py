# -*- coding: utf-8 -*-
# Author: Maximiliano Rocamora / maxirocamora@gmail.com
# Mini Panel for Maya Reference control

'''
1.0.0 : first version 06/2018
1.1.0 : arcaneQt
1.2.0 : removed arcaneQt
'''

VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_PATCH = 0

version = '{}.{}.{}'.format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
__version__ = version

__app__ = 'RP'
__qt__ = 'Arcane:Qt_' + __app__ + '_ui'

__all__ = ['version', '__version__', '__app__', '__qt__']
