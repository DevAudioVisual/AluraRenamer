import os
import tkinter as tk
from tkinter import filedialog, messagebox
import re
from tkinter import ttk
import webbrowser
from PIL import Image
from Util import Util
import Util.CustomWidgets as ctk
import Util.Styles as Styles
import customtkinter as ctkk
import urllib.error
import pandas as pd
import re

dados = {} 

def buscar_na_planilha():
    global dados 

    spreadsheet_url = link_planilha_entry.get() 
    if spreadsheet_url:
        padrao_id = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
        match = re.search(padrao_id, spreadsheet_url)
        if match:
            spreadsheet_id = match.group(1)
            csv_export_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'

            try:
                df = pd.read_csv(csv_export_url, header=None)

                coluna_a = df.iloc[:, 0]
                coluna_b = df.iloc[:, 1]

                padrao_aula = r"Aula \d+\.\d+"

                for i in range(len(coluna_a)):
                    if pd.notna(coluna_a[i]) and re.search(padrao_aula, str(coluna_a[i])):
                        dados[coluna_a[i]] = coluna_b[i]

                #for aula, nome in dados.items():
                    #print(f"Aula: {aula}, Nome: {nome}")

                atualizar_entradas_videos()

            except pd.errors.EmptyDataError:
                messagebox.showerror("Erro", "A planilha está vazia.")
            except pd.errors.ParserError:
                messagebox.showerror("Erro", "Erro ao analisar a planilha. Verifique se o formato está correto.")
            except IndexError:
                messagebox.showerror("Erro", "A planilha não tem colunas suficientes. Verifique se há pelo menos duas colunas.")
            except urllib.error.URLError:
                messagebox.showerror("Erro", "Erro ao acessar a planilha. Verifique sua conexão com a internet e tente novamente mais tarde.")

        else:
            messagebox.showerror("Erro", "Não foi possível extrair o ID da planilha a partir do link fornecido.")

def atualizar_entradas_videos():
    global entradas_videos

    for arquivo, entrada_nome in entradas_videos.items():
        nome_sem_extensao, _ = os.path.splitext(arquivo)
        numero_aula_video = nome_sem_extensao.split('-')[0]

        nome_aula = dados.get(f"Aula {numero_aula_video}", "")
        if nome_aula:
            entrada_nome.getEntry().delete(0, tk.END)
            entrada_nome.getEntry().insert(0, nome_aula)
            #entrada_nome.getEntry().configure(state='readonly')
        else:
            entrada_nome.getEntry().configure(state='normal')


def selecionar_pasta():
    global entradas_videos
    pasta = filedialog.askdirectory()
    quantidade = 0
    if pasta:
        for widget in frame_videos.winfo_children():
            widget.destroy()

        entradas_videos = {}

        for arquivo in os.listdir(pasta):
            if arquivo.endswith(('.mp4', '.avi', '.mkv','.mov')):
                quantidade +=1
                frame_video = ctk.CustomFrame(frame_videos)
                frame_video.pack(fill="x")

                nome_sem_extensao, _ = os.path.splitext(arquivo)
                numero_aula_video = nome_sem_extensao.split('-')[0]

                if not re.match(r"^\d+\.\d+$", numero_aula_video):
                    label_texto = f"{arquivo} (Nomenclatura inválida!)"
                    ctk.CustomLabel(frame_video, text=label_texto,text_color="red").pack(side=tk.LEFT,fill="x",pady=5)
                else:
                    ctk.CustomLabel(frame_video, text=arquivo).pack(side=tk.LEFT,fill="x",pady=5)
                    entrada_nome = ctk.CustomEntry(frame_video,width=300)
                    entrada_nome.pack(side=tk.LEFT,fill="x",padx=5)

                    nome_aula = dados.get(f"Aula {numero_aula_video}", "")
                    if nome_aula:
                        entrada_nome.getEntry().insert(0, nome_aula)
                        #entrada_nome.getEntry().configure(state='readonly')
                    else:
                        entrada_nome.getEntry().configure(state='normal')

                    entradas_videos[arquivo] = entrada_nome

        pasta_selecionada.set(pasta)
        RenomearB.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        valor = quantidade * 95 if quantidade <= 750 else 750
        print(valor)
        frame_videos.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        #janela.geometry(f"600x{valor}")
        janela.geometry(f"600x750")
        janela.update()

def renomear_videos():
    global entradas_videos
    pasta = pasta_selecionada.get()
    id_curso = id_curso_entry.get()

    if not pasta:
        messagebox.showerror("Erro", "Selecione uma pasta.")
        return
    if not id_curso:
        messagebox.showerror("Erro", "Defina um ID do curso.")
        return
    if not entradas_videos:
        messagebox.showerror("Erro", "Nenhum video encontrado ou nomenclatura inválida.\nFormatos compativeis: .mp4, .avi, .mkv, .mov\nNomenclatura correta: #.#")
        return

    for arquivo_original, entrada_nome in entradas_videos.items():
        novo_nome = entrada_nome.get()
        if novo_nome:
            nome_sem_extensao, extensao = os.path.splitext(arquivo_original) 
            numero_aula_video = nome_sem_extensao.split('-')[0] 
            novo_nome_arquivo = f"{id_curso}-video{numero_aula_video}-{novo_nome}{extensao}" 
            caminho_antigo = os.path.join(pasta, arquivo_original)
            caminho_novo = os.path.join(pasta, novo_nome_arquivo)
            os.rename(caminho_antigo, caminho_novo)

    messagebox.showinfo("Sucesso", "Vídeos renomeados com sucesso!")

janela = tk.Tk()
janela.title("S_AluraRename")
Styles.DefiniEstilo(ttk)
icone = Util.pegarImagem("icon.ico")
janela.iconbitmap(icone)
janela.geometry("600x170")
janela.resizable(False,False)
janela.update()
janela.configure(bg=Styles.cor_fundo)


pasta_selecionada = tk.StringVar()

framePrincipal = ctk.CustomFrame(janela)
framePrincipal.pack(padx=10,pady=10)

ctk.CustomLabel(framePrincipal, text="Pasta:").grid(row=0, column=0, padx=5, pady=5)
ctk.CustomEntry(framePrincipal, textvariable=pasta_selecionada, state='readonly',width=300).grid(row=0, column=1, pady=5)
ctk.CustomButton(framePrincipal, text="Selecionar Pasta", command=selecionar_pasta).grid(row=0, column=2, padx=5, pady=5)

frame_videos = ctk.CustomScroolabeFrame(framePrincipal)


ctk.CustomLabel(framePrincipal, text="ID do Curso:").grid(row=1, column=0, padx=5, pady=5)
id_curso_entry = ctk.CustomEntry(framePrincipal,width=300)
id_curso_entry.grid(row=1, column=1, padx=5, pady=5)
dropVar = tk.StringVar(value="#.#")
ctk.CustomComboBox(framePrincipal,Values=["#.#"],variable=dropVar).grid(row=1, column=2, padx=5, pady=5)

ctk.CustomLabel(framePrincipal, text="Link da planilha:").grid(row=2, column=0, padx=5, pady=5)
link_planilha_entry = ctk.CustomEntry(framePrincipal,width=300)
link_planilha_entry.grid(row=2, column=1, padx=5, pady=5)
ctk.CustomButton(framePrincipal, text="Buscar", command=buscar_na_planilha).grid(row=2, column=2, padx=5, pady=5)

RenomearB = ctk.CustomButton(framePrincipal, text="Renomear Vídeos", command=renomear_videos)
RenomearB.grid_forget()

credits_frame = tk.Frame(janela, bg="gray")
credits_frame.pack(fill="x",side="bottom")

def abrir_link(event):
    webbrowser.open_new("https://samuelmariano.com/s-alurarename")

imagemSamuel = ctkk.CTkImage(dark_image=Image.open(Util.pegarImagem("penguin.png")), light_image=Image.open(Util.pegarImagem("penguin.png")), size=(25, 25))
label_autor = ctkk.CTkLabel(credits_frame, text="Por: Samuel Mariano", font=Styles.fonte_texto,cursor="hand2", image=imagemSamuel, compound="right", text_color="white")
label_autor.pack(anchor="center", pady=5)
label_autor.bind("<Button-1>", abrir_link)

janela.mainloop()