import os
import re
from tkinter import filedialog, messagebox
import Util.CustomWidgets as ctk
import pandas as pd
import urllib.error
import tkinter as tk


class App():
    def __init__(self, root, **kwargs):
        self.root = root
        self.dados = {}
        self.frame_videos = None
        self.pasta_selecionada = None
        self.RenomearB = None
        self.id_curso_entry = None

    def setFrameVideos(self, frame_videos):
        self.frame_videos = frame_videos

    def setid_curso_entry(self, id_curso_entry):
        self.id_curso_entry = id_curso_entry

    def setPastaSelecionada(self, pasta_selecionada):
        self.pasta_selecionada = pasta_selecionada

    def setRenomearB(self, RenomearB):
        self.RenomearB = RenomearB

    def buscar_na_planilha(self, link_planilha_entry):
        spreadsheet_url = link_planilha_entry.get()
        if spreadsheet_url:
            padrao_id = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
            match = re.search(padrao_id, spreadsheet_url)
            if match:
                spreadsheet_id = match.group(1)
                csv_export_url = f'https://docs.google.com/spreadsheets/d/{
                    spreadsheet_id}/export?format=csv'

                try:
                    df = pd.read_csv(csv_export_url, header=None)

                    coluna_a = df.iloc[:, 0]
                    coluna_b = df.iloc[:, 1]

                    padrao_aula = r"Aula \d+\.\d+"

                    for i in range(len(coluna_a)):
                        if pd.notna(coluna_a[i]) and re.search(padrao_aula, str(coluna_a[i])):
                            self.dados[coluna_a[i]] = coluna_b[i]

                    # for aula, nome in dados.items():
                        # print(f"Aula: {aula}, Nome: {nome}")

                    self.atualizar_entradas_videos()

                except pd.errors.EmptyDataError:
                    messagebox.showerror("Erro", "A planilha está vazia.")
                except pd.errors.ParserError:
                    messagebox.showerror(
                        "Erro", "Erro ao analisar a planilha. Verifique se o formato está correto.")
                except IndexError:
                    messagebox.showerror(
                        "Erro", "A planilha não tem colunas suficientes. Verifique se há pelo menos duas colunas.")
                except urllib.error.URLError:
                    messagebox.showerror(
                        "Erro", "Erro ao acessar a planilha. Verifique sua conexão com a internet e tente novamente mais tarde.")

            else:
                messagebox.showerror(
                    "Erro", "Não foi possível extrair o ID da planilha a partir do link fornecido.")

    def atualizar_entradas_videos(self):
        global entradas_videos

        for arquivo, entrada_nome in entradas_videos.items():
            nome_sem_extensao, _ = os.path.splitext(arquivo)
            numero_aula_video = nome_sem_extensao.split('-')[0]

            nome_aula = self.dados.get(f"Aula {numero_aula_video}", "")
            if nome_aula:
                entrada_nome.getEntry().delete(0, tk.END)
                entrada_nome.getEntry().insert(0, nome_aula)
                # entrada_nome.getEntry().configure(state='readonly')
            else:
                entrada_nome.getEntry().configure(state='normal')

    def selecionar_pasta(self):
        global entradas_videos
        pasta = filedialog.askdirectory()
        quantidade = 0
        if pasta:
            for widget in self.frame_videos.winfo_children():
                widget.destroy()

            entradas_videos = {}

            for arquivo in os.listdir(pasta):
                if arquivo.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                    quantidade += 1
                    frame_video = ctk.CustomFrame(self.frame_videos)
                    frame_video.pack(fill="x")

                    nome_sem_extensao, _ = os.path.splitext(arquivo)
                    numero_aula_video = nome_sem_extensao.split('-')[0]

                    if not re.match(r"^\d+\.\d+$", numero_aula_video):
                        label_texto = f"{arquivo} (Nomenclatura inválida!)"
                        ctk.CustomLabel(frame_video, text=label_texto, text_color="red").pack(
                            side=tk.LEFT, fill="x", pady=5)
                    else:
                        ctk.CustomLabel(frame_video, text=arquivo).pack(
                            side=tk.LEFT, fill="x", pady=5)
                        entrada_nome = ctk.CustomEntry(frame_video, width=300)
                        entrada_nome.pack(side=tk.LEFT, fill="x", padx=5)

                        nome_aula = self.dados.get(
                            f"Aula {numero_aula_video}", "")
                        if nome_aula:
                            entrada_nome.getEntry().insert(0, nome_aula)
                            # entrada_nome.getEntry().configure(state='readonly')
                        else:
                            entrada_nome.getEntry().configure(state='normal')

                        entradas_videos[arquivo] = entrada_nome

            self.pasta_selecionada.set(pasta)
            self.RenomearB.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
            valor = quantidade * 95 if quantidade <= 750 else 750
            print(valor)
            self.frame_videos.grid(
                row=3, column=0, columnspan=3, padx=5, pady=5)
            # janela.geometry(f"600x{valor}")
            self.root.geometry(f"600x750")
            self.root.update()

    def renomear_videos(self):
        global entradas_videos
        pasta = self.pasta_selecionada.get()
        id_curso = self.id_curso_entry.get()

        if not pasta:
            messagebox.showerror("Erro", "Selecione uma pasta.")
            return
        if not id_curso:
            messagebox.showerror("Erro", "Defina um ID do curso.")
            return
        if not entradas_videos:
            messagebox.showerror(
                "Erro", "Nenhum video encontrado ou nomenclatura inválida.\nFormatos compativeis: .mp4, .avi, .mkv, .mov\nNomenclatura correta: #.#")
            return

        for arquivo_original, entrada_nome in entradas_videos.items():
            novo_nome = entrada_nome.get()
            if novo_nome:
                nome_sem_extensao, extensao = os.path.splitext(
                    arquivo_original)
                numero_aula_video = nome_sem_extensao.split('-')[0]
                novo_nome_arquivo = f"{
                    id_curso}-video{numero_aula_video}-{novo_nome}{extensao}"
                caminho_antigo = os.path.join(pasta, arquivo_original)
                caminho_novo = os.path.join(pasta, novo_nome_arquivo)
                os.rename(caminho_antigo, caminho_novo)

        messagebox.showinfo("Sucesso", "Vídeos renomeados com sucesso!")
