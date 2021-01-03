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
                "Game_Control_Dev_ver_2/haarcascade_eye.xml",
                "Game_Control_Dev_ver_2/haarcascade_frontalface_default.xml"
                #"nn"
            ]
        }},
    executables=executables
)
