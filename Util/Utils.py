import logging
import os
from pathlib import Path
import subprocess
import sys
from tkinter import messagebox
from urllib.parse import urlparse

version = "V0.0"

global diretorio_atual
global icone
diretorio_atual = Path(__file__).parent.absolute()
icone = os.path.join(diretorio_atual, 'icon.ico')


def reabrir():
    try:
        if getattr(sys, 'frozen', False):  # If the program is compiled as an executable
            executable = sys.executable
            subprocess.Popen([executable])
        else:
            subprocess.Popen([sys.executable] + sys.argv)
    finally:
        sys.exit()


def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def quebrar_linhas(texto, max_comprimento=80):
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 > max_comprimento:
            linhas.append(linha_atual)
            linha_atual = palavra
        else:
            if linha_atual:
                linha_atual += " "
            linha_atual += palavra

    if linha_atual:
        linhas.append(linha_atual)

    return "\n".join(linhas)


def pegarImagem(imagem):
    return os.path.join("Assets", imagem)


def logWarning(func, mensagem, dialog=True):
    logging.warn(f"Aviso na função {func} ", quebrar_linhas(mensagem))
    print(f"Aviso na função {func} ", quebrar_linhas(mensagem))
    if dialog:
        messagebox.showwarning("Aviso", mensagem)


def logInfo(func, mensagem, dialog=True):
    logging.debug(f"Info na função {func} ", quebrar_linhas(mensagem))
    print(f"Info na função {func} ", quebrar_linhas(mensagem))
    if dialog:
        messagebox.showwarning("Info", mensagem)


def LogError(func, mensagem, dialog=True):
    print(f"Erro na função {func} ", quebrar_linhas(mensagem))
    logging.error(f"Erro na função {func} ", quebrar_linhas(mensagem))
    if dialog:
        messagebox.showwarning("Erro", quebrar_linhas(mensagem))
