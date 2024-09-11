from Models import ModelRenomeador, Updates
import Util.Styles as Styles
import customtkinter as ctkk
from tkinter import ttk
import webbrowser
from PIL import Image
from Util import Utils
import tkinter as tk
import Util.CustomWidgets as ctk

root = tk.Tk()


class App():
    def __init__(self, **kwargs):
        self.setupRoot()
        self.Model = ModelRenomeador.App(root=root)

    def setupInterface(self):
        pasta_selecionada = tk.StringVar()
        self.Model.setPastaSelecionada(pasta_selecionada)

        framePrincipal = ctk.CustomFrame(root)
        framePrincipal.pack(padx=10, pady=10)

        ctk.CustomLabel(framePrincipal, text="Vídeos:").grid(row=0, column=0, padx=5, pady=5)
        ctk.CustomEntry(framePrincipal, textvariable=pasta_selecionada,state='readonly', width=300).grid(row=0, column=1, pady=5)
        ctk.CustomButton(framePrincipal, text="Selecionar Vídeos",command=self.Model.selecionar_arquivos).grid(row=0, column=2, padx=5, pady=5)


        ctk.CustomLabel(framePrincipal, text="Planilha:").grid(row=1, column=0, padx=5, pady=5)
        link_planilha_entry = ctk.CustomEntry(framePrincipal, width=300)
        link_planilha_entry.grid(row=1, column=1, padx=5, pady=5)
        ctk.CustomButton(framePrincipal, text="Buscar", command=lambda: self.Model.buscar_na_planilha(link_planilha_entry)).grid(row=1, column=2, padx=5, pady=5)
        
        ctk.CustomLabel(framePrincipal, text="ID do Curso:").grid(row=2, column=0, padx=5, pady=5)
        id_curso_entry = ctk.CustomEntry(framePrincipal, width=300)
        self.Model.setid_curso_entry(id_curso_entry)
        id_curso_entry.grid(row=2, column=1, padx=5, pady=5)
        formatosVar = tk.StringVar(value="#.#")
        ctk.CustomComboBox(framePrincipal, Values=["#.#"], variable=formatosVar).grid(row=2, column=2, padx=5, pady=5)
        
        ctk.CustomLabel(framePrincipal, text="Sufixo:").grid(row=3, column=0, padx=5, pady=5)
        sufixo = ctk.CustomEntry(framePrincipal, width=300)
        self.Model.setSufixo(sufixo)
        sufixo.grid(row=3, column=1, padx=5, pady=5)
        sufixosVar = tk.StringVar(value=" ")
        ctk.CustomComboBox(framePrincipal, variable=sufixosVar).grid(row=3, column=2, padx=5, pady=5)


        frame_videos = ctk.CustomScroolabeFrame(framePrincipal)
        self.Model.setFrameVideos(frame_videos)
            

        RenomearB = ctk.CustomButton(framePrincipal, text="Renomear Vídeos", command=self.Model.renomear_videos)
        self.Model.setRenomearB(RenomearB)
        RenomearB.grid_forget()


        root.after(2000, lambda: Updates.app())
        root.mainloop()

    def setupRoot(self):
        root.title("AluraRenamer " + Utils.version)
        Styles.DefiniEstilo(ttk)
        icone = Utils.pegarImagem("icon.ico")
        root.iconbitmap(icone)
        root.geometry("600x170")
        root.resizable(False, False)
        root.update()
        root.configure(bg=Styles.cor_fundo)
