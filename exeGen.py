"""
    Selle skriptiga saab genereerida executable mängu jaoks.

    cx_Freexe installimiseks:
    pip install cx_Freeze --upgrade

    Skripti käivitamiseks jooksvas kaustas:
    python exeGen.py build

    Tulemusena tekib kaust build.
"""

import cx_Freeze

executables = [cx_Freeze.Executable("TheGame.py")]

cx_Freeze.setup(
    name="The Game",
    options={
        "build_exe": {"packages": [
            "pygame"
        ],
            "include_files": [
                "pildid",
                "face_command_details"
                #"nn"
            ]
        }},
    executables=executables
)
