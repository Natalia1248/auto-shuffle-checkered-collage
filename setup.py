import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('double click me.py', base=base, icon='icon.ico')
]


buildOptions = dict(zip_include_packages=["*"], zip_exclude_packages=[])

setup(name='checkered collage-o-matic',
      version='0.1',
      executables=executables,
      options = {
        'build_exe': {
            'build_exe': './/build'
            }
        }

      )
