from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
#buildOptions = dict(packages = [], excludes = [])

Include_Modules = [
    "tkinter","openpyxl","time", "datetime"
]

Exclude_Modules = [
    "ipykernel", "iPython", "ipython_genutils", "matplotlib", "pandas", "scipy", "lib2to3", "jupyter_client",
    "jupyter_core", "tcl8.6/tzdata", "nose", "unittest", "pkg_resources", "pexpect", "setuptools"
]

buildOptions = {"includes": Include_Modules, "include_files": ["mouse_face.ico"],
                "excludes": Exclude_Modules,
                }

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('respiration_tracker.py', base=base, icon="mouse_face.ico")
]

setup(name='Respiration Tracker',
      version = '1.0',
      description = 'Interfaces with an arduino to track rodent respiration',
      options = dict(build_exe = buildOptions),
      executables = executables)
