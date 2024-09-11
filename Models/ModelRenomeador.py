import os
import re
import time
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import requests
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
        self.id_curso = None
        self.id_curso_entry = None
        self.sufixo = None
        
        self.entradas_videos = None

    def setFrameVideos(self, frame_videos):
        self.frame_videos = frame_videos
    
    def setSufixo(self, sufixo):
        self.sufixo = sufixo
    
    def setid_curso_entry(self, id_curso_entry):
        self.id_curso_entry = id_curso_entry

    def setPastaSelecionada(self, pasta_selecionada):
        self.pasta_selecionada = pasta_selecionada

    def setRenomearB(self, RenomearB):
        self.RenomearB = RenomearB

    def buscar_na_planilha(self, link_planilha_entry):
        spreadsheet_url = link_planilha_entry.get()
        if self.entradas_videos == None:
            messagebox.showerror("Erro", "Nenhum arquivo de vídeo fornecido.")
            return  
        def extrair_titulo_planilha(url_planilha):
            try:
                # Faz a requisição à página da planilha
                response = requests.get(url_planilha)
                response.raise_for_status()  # Lança uma exceção se houver erro na requisição

                # Analisa o HTML da página
                soup = BeautifulSoup(response.content, 'html.parser')

                # Tenta encontrar o título na estrutura HTML (pode precisar ajustar isso)
                titulo_elemento = soup.find('title')
                if titulo_elemento:
                    titulo = titulo_elemento.text.strip()
                    # Remove o sufixo "- Google Sheets" se existir
                    titulo = titulo.replace(" - Google Sheets", "")
                    padrao = r"^\d{4}"  # Expressão regular para encontrar 4 dígitos no início da string
                    correspondencia = re.match(padrao, titulo)
                    return correspondencia.group(0)
                else:
                    return None  # Retorna None se não encontrar o título

            except requests.exceptions.RequestException as e:
                print(f"Erro ao acessar a página: {e}")
                return None
        if spreadsheet_url:
            #print("#######################",extrair_titulo_planilha(spreadsheet_url))
            #self.setid_curso_entry(extrair_titulo_planilha(spreadsheet_url))
            self.id_curso_entry.getEntry().delete(0, tk.END)  # Limpa o conteúdo atual
            self.id_curso_entry.getEntry().insert(0, extrair_titulo_planilha(spreadsheet_url))  # Insere o novo texto
            self.frame_videos.update()
            self.id_curso_entry.getEntry().update()
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
        for arquivo, entrada_nome in self.entradas_videos.items():
            nome_sem_extensao, _ = os.path.splitext(os.path.basename(arquivo))
            numero_aula_video = nome_sem_extensao.split('-')[0]

            nome_aula = self.dados.get(f"Aula {numero_aula_video}", "")
            if nome_aula:
                entrada_nome.getEntry().delete(0, tk.END)
                entrada_nome.getEntry().insert(0, nome_aula)
                # entrada_nome.getEntry().configure(state='readonly')
            else:
                entrada_nome.getEntry().configure(state='normal')

    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfiles(mode='r', filetypes=[('Arquivos de vídeo', '*.mp4 *.avi *.mkv *.mov')])
        quantidade = 0
        if arquivos:
            self.entradas_videos = {}
            for widget in self.frame_videos.winfo_children():
                widget.destroy()
     

            for arquivo in arquivos:
                #if arquivo.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                    quantidade += 1
                    frame_video = ctk.CustomFrame(self.frame_videos)
                    frame_video.pack(fill="x")

                    nome_sem_extensao, _ = os.path.splitext(os.path.basename(arquivo.name))
                    numero_aula_video = nome_sem_extensao.split('-')[0]

                    if not re.match(r"^\d+\.\d+$", numero_aula_video):
                        label_texto = f"{os.path.basename(arquivo.name)} (Nomenclatura inválida!)"
                        ctk.CustomLabel(frame_video, text=label_texto, text_color="red").pack(
                            side=tk.LEFT, fill="x", pady=5)
                    else:
                        ctk.CustomLabel(frame_video, text=os.path.basename(arquivo.name)).pack(
                            side=tk.LEFT, fill="x", pady=5)
                        entrada_nome = ctk.CustomEntry(frame_video, width=300)
                        entrada_nome.pack(side=tk.LEFT, fill="x", padx=5)

                        nome_aula = self.dados.get(f"Aula {numero_aula_video}", "")
                        if nome_aula:
                            entrada_nome.getEntry().insert(0, nome_aula)
                            # entrada_nome.getEntry().configure(state='readonly')
                        else:
                            entrada_nome.getEntry().configure(state='normal')

                        self.entradas_videos[os.path.basename(arquivo.name)] = entrada_nome

            self.pasta_selecionada.set(os.path.dirname(arquivos[0].name))
            self.RenomearB.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
            valor = quantidade * 95 if quantidade <= 750 else 750
            print(valor)
            self.frame_videos.grid(
                row=4, column=0, columnspan=3, padx=5, pady=5)
            # janela.geometry(f"600x{valor}")
            self.root.geometry(f"600x750")
            self.root.update()

    def renomear_videos(self):
        pasta = self.pasta_selecionada.get()
        id_curso = self.id_curso_entry.get()
        sufixo = self.sufixo.get()
        erro = False

        if not pasta:
            messagebox.showerror("Erro", "Selecione uma pasta.")
            return
        if not id_curso:
            messagebox.showerror("Erro", "Defina um ID do curso.")
            return
        if not self.entradas_videos or None:
            messagebox.showerror(
                "Erro", "Nenhum video encontrado ou nomenclatura inválida.\nFormatos compativeis: .mp4, .avi, .mkv, .mov\nNomenclatura correta: #.#")
            return

        for arquivo_original, entrada_nome in self.entradas_videos.items():
            novo_nome = entrada_nome.get()
            arquivo_original_tratado = arquivo_original
            if novo_nome:
                nome_sem_extensao, extensao = os.path.splitext(arquivo_original_tratado)
                numero_aula_video = nome_sem_extensao.split('-')[0]
                novo_nome_arquivo = f"{id_curso}-video{numero_aula_video}-{novo_nome}-{sufixo}{extensao}" if sufixo else f"{id_curso}-video{numero_aula_video}-{novo_nome}{extensao}"
                caminho_antigo = os.path.join(pasta, arquivo_original_tratado)
                caminho_novo = os.path.join(pasta, novo_nome_arquivo)
                MAX_TENTATIVAS = 2
                TEMPO_ESPERA = 1
                for tentativa in range(MAX_TENTATIVAS):
                    try:
                        os.rename(os.path.normpath(caminho_antigo), os.path.normpath(caminho_novo))
                        break  
                    except PermissionError as e:
                        if tentativa < MAX_TENTATIVAS - 1:
                            print(f"Tentativa {tentativa + 1} falhou. Aguardando {TEMPO_ESPERA} segundos...")
                            time.sleep(TEMPO_ESPERA)
                        else:
                            erro = True
                            print(f"Erro: Não foi possível renomear o arquivo {caminho_antigo} após {MAX_TENTATIVAS} tentativas. {e}")
        if erro == False:
            messagebox.showinfo("Sucesso", "Vídeos renomeados com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possivel renomear os arquivos.")
