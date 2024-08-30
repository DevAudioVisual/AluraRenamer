
import sys
from cx_Freeze import setup, Executable

#qt_platforms_path = os.path.join(os.environ['VIRTUAL_ENV'], 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins', 'platforms')
build_exe_options = {
    #"packages": ["os", "shutil", "tkinter", "patoolib", "numpy", "pandas", "pystray", "PyQt5", "requests", "six", "tqdm", "filelock","setuptools"],
    "include_files": ["Imagens"],
    "include_msvcr": True,
    #"includes": ["PyQt5.sip","moviepy.audio.fx.all"],
    #"bin_includes": ["msvcp140.dll", "tbb12.dll"],
    #"bin_path_includes": ["C:\\Windows\\System32","C:\\Windows\\SysWOW64", "C:\\Arquivos de Programas\\Intel\\TBB\\bin","C:\\Program Files (x86)\\Intel\\oneAPI\\tbb\\2021.13\\bin"]
}


# Adiciona a opção de base "Win32GUI" para esconder a janela de console no Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Adiciona o ícone ao executável
executables = [
    Executable(
        "Main.py",
        icon=r"Imagens\icon.ico",
        base=base,
        target_name="S_AluraRename",
    )
]

setup(
    name="S_AluraRename",
    version=1.0,
    description="Renomeador de vídeos Alura", 
    options={"build_exe": build_exe_options},
    executables=executables,
)
