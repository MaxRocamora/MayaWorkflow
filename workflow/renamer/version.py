# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
'''
3dsmax style renamer
Max Rocamora / maxirocamora@gmail.com
1.0.0 Release 12/09/2015
version 1.1 - bug fix on groups names and clashing - 18/05/16
version 1.2 - bug on long names internal - 20/10/16
version 1.5 - using UUID for nested names bug - 22/08/17
version 2.0 - maya 2018
version 3.0 - reworked, added undo wrapper and replace string method
version 3.2 - integrated ui with arcane
version 3.3.0 : arcaneQt
version 3.3.1 - about window fix
version 3.5.0 - removed arcaneQt
version 3.6.0 - stand alone tool, moved to workflow repository

'''

VERSION_MAJOR = 3
VERSION_MINOR = 6
VERSION_PATCH = 0

version = '{}.{}.{}'.format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
__version__ = version

__app__ = 'Renamer'
__qt__ = 'Arcane2:Qt_' + __app__ + '_ui'

__all__ = ['version', '__version__', '__app__', '__qt__']
