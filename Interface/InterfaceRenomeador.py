from Models import ModelRenomeador
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

        ctk.CustomLabel(framePrincipal, text="Pasta:").grid(
            row=0, column=0, padx=5, pady=5)
        ctk.CustomEntry(framePrincipal, textvariable=pasta_selecionada,
                        state='readonly', width=300).grid(row=0, column=1, pady=5)
        ctk.CustomButton(framePrincipal, text="Selecionar Pasta",
                         command=self.Model.selecionar_pasta).grid(row=0, column=2, padx=5, pady=5)

        frame_videos = ctk.CustomScroolabeFrame(framePrincipal)
        self.Model.setFrameVideos(frame_videos)

        ctk.CustomLabel(framePrincipal, text="ID do Curso:").grid(
            row=1, column=0, padx=5, pady=5)
        id_curso_entry = ctk.CustomEntry(framePrincipal, width=300)
        self.Model.setid_curso_entry(id_curso_entry)
        id_curso_entry.grid(row=1, column=1, padx=5, pady=5)
        dropVar = tk.StringVar(value="#.#")
        ctk.CustomComboBox(framePrincipal, Values=["#.#"], variable=dropVar).grid(
            row=1, column=2, padx=5, pady=5)

        ctk.CustomLabel(framePrincipal, text="Link da planilha:").grid(
            row=2, column=0, padx=5, pady=5)
        link_planilha_entry = ctk.CustomEntry(framePrincipal, width=300)
        link_planilha_entry.grid(row=2, column=1, padx=5, pady=5)

        def buscar():
            self.Model.buscar_na_planilha(link_planilha_entry)
        ctk.CustomButton(framePrincipal, text="Buscar", command=buscar).grid(
            row=2, column=2, padx=5, pady=5)

        RenomearB = ctk.CustomButton(
            framePrincipal, text="Renomear Vídeos", command=self.Model.renomear_videos)
        self.Model.setRenomearB(RenomearB)
        RenomearB.grid_forget()

        credits_frame = tk.Frame(root, bg="gray")
        credits_frame.pack(fill="x", side="bottom")

        imagemSamuel = ctkk.CTkImage(dark_image=Image.open(Utils.pegarImagem(
            "penguin.png")), light_image=Image.open(Utils.pegarImagem("penguin.png")), size=(25, 25))
        label_autor = ctkk.CTkLabel(credits_frame, text="Por: Samuel Mariano", font=Styles.fonte_texto,
                                    cursor="hand2", image=imagemSamuel, compound="right", text_color="white")
        label_autor.pack(anchor="center", pady=5)
        label_autor.bind("<Button-1>", self.abrir_link_site)

        root.mainloop()

    def setupRoot(self):
        root.title("S_AluraRename")
        Styles.DefiniEstilo(ttk)
        icone = Utils.pegarImagem("icon.ico")
        root.iconbitmap(icone)
        root.geometry("600x170")
        root.resizable(False, False)
        root.update()
        root.configure(bg=Styles.cor_fundo)

    def abrir_link_site(event):
        webbrowser.open_new("https://samuelmariano.com/s-alurarename")
