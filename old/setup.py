import os
import sys
from cx_Freeze import setup, Executable

sys.path.append(os.getcwd())

build_exe_options = {
    "packages": ["pytubefix", "moviepy", "tkinter", "PySimpleGUI"],
    "includes": ["tkinter"],
    "include_files": ["sources"],
}

if __name__ == "__main__":
    setup(
        name="YouTube Download",
        version="1.0",
        options={"build_exe": build_exe_options},
        description="Baixa videos e audios do Youtube",
        executables=[
            Executable(
                "main.py", base="Win32GUI",
            )
        ],
    )
