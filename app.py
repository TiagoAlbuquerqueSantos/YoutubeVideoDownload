
import os
import threading
import customtkinter as ctk
from tkinter import messagebox
from pytubefix import YouTube
from moviepy import AudioFileClip


def sanitize_filename(filename):
    return "".join(c if c.isalnum() else "_" for c in filename)

def get_available_resolutions(streams):
    resolutions = sorted({stream.resolution for stream in streams.filter(progressive=True)}, key=lambda x: int(x[:-1]))
    return resolutions

def get_available_audio_qualities(streams):
    qualities = sorted({stream.abr for stream in streams.filter(only_audio=True)}, key=lambda x: int(x[:-4]))
    return qualities


class DownloadVideo(ctk.CTkToplevel):
    def __init__(self, on_complete_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('')
        self.geometry('400x250')
        self.resizable(False, False)
        self.on_complete_callback = on_complete_callback
        self.download_complete = False

        ctk.CTkLabel(
            self,
            text='Baixando Vídeo...',
            width=150,
            height=30,
        ).place(relx=0.5, rely=0.15, anchor='center')

        self.barra_progresso = ctk.CTkProgressBar(
            self,
            orientation='horizontal',
            indeterminate_speed=0.5,
            mode='indeterminate',
            width=300,
        )
        self.barra_progresso.place(relx=0.5, rely=0.4, anchor='center')
        self.barra_progresso.start()

        self.status_label = ctk.CTkLabel(
            self,
            text='Preparando download...',
            width=300,
            height=30,
        )
        self.status_label.place(relx=0.5, rely=0.65, anchor='center')

        self.btn_concluir = ctk.CTkButton(
            self,
            text='Concluir',
            width=140,
            height=30,
            border_width=1,
            command=self.fechar_janela,
            state='disabled'
        )
        self.btn_concluir.place(relx=0.47, rely=0.9, anchor='se')

        self.btn_cancelar = ctk.CTkButton(
            self,
            text='Cancelar',
            width=140,
            height=30,
            border_width=1,
            command=self.fechar_janela,
        )
        self.btn_cancelar.place(relx=0.53, rely=0.9, anchor='sw')

    def update_status(self, message):
        self.status_label.configure(text=message)

    def download_complete_ui(self):
        self.download_complete = True
        self.barra_progresso.stop()
        self.status_label.configure(text='Download concluído com sucesso!')
        self.btn_concluir.configure(state='normal')
        self.btn_cancelar.configure(text='Fechar')

    def download_error_ui(self, error_message):
        self.barra_progresso.stop()
        self.status_label.configure(text=f'Erro: {error_message}')
        self.btn_cancelar.configure(text='Fechar')

    def fechar_janela(self):
        if self.on_complete_callback and self.download_complete:
            self.on_complete_callback()
        self.destroy()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.video_stream = None
        self.segunda_janela = None

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('themes/Cobalt.json')

        self.geometry('540x350')
        self.grid_columnconfigure([0], weight=1)
        self.grid_rowconfigure([0], weight=1)
        self.title('Baixador de vídeos do Youtube')
        self.resizable(False, False)

        self.conteudo = ctk.CTkFrame(self, border_width=1)

        self.frame_layout_1 = ctk.CTkFrame(self.conteudo, border_width=1)
        self.frame_layout_2 = ctk.CTkFrame(self.conteudo, border_width=1)
        self.frame_layout_3 = ctk.CTkFrame(self.conteudo, border_width=1)

        self.conteudo.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_layout_1.grid_columnconfigure(0, weight=1)
        self.frame_layout_2.grid_columnconfigure(0, weight=1)
        self.frame_layout_3.grid_columnconfigure(0, weight=1)

        self.conteudo.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.frame_layout_1.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.frame_layout_2.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.frame_layout_3.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        self.url_video = ctk.CTkEntry(
            self.conteudo,
            placeholder_text='Digite a URL do Youtube',
            border_width=1,
            height=30
        )
        self.url_video.grid(row=0, column=0, padx=10, pady=10, sticky='ew', columnspan=3)

        ctk.CTkLabel(
            self.frame_layout_1,
            text='Formato do Arquivo',
            corner_radius=6,
            fg_color='gray30',
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(
            self.frame_layout_2,
            text='Resolução do Vídeo',
            corner_radius=6,
            fg_color='gray30',
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(
            self.frame_layout_3,
            text='Config. de Áudio',
            corner_radius=6,
            fg_color='gray30',
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.formato_arquivo = ctk.CTkOptionMenu(
            self.frame_layout_1,
            values=['mp4', 'mp3'],
            width=150,
            height=30,
            command=self.esconder_menu_res_video,
        )
        self.formato_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.res_video = ctk.CTkOptionMenu(
            self.frame_layout_2,
            values=['720p', '360p'],
            width=150,
            height=30,
        )
        self.res_video.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.config_audio = ctk.CTkOptionMenu(
            self.frame_layout_3,
            values=['128kbps', '144kbps'],
            width=150,
            height=30,
            state='disabled',
        )
        self.config_audio.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.btn = ctk.CTkButton(
            self.conteudo,
            text='Baixar',
            width=160,
            height=30,
            border_width=1,
            command=self.abrir_segunda_janela,
        )
        self.btn.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.texto = ctk.CTkLabel(
            self,
            text='Digite a URL do vídeo do Youtube que deseja baixar,'
                 ' escolha o formato do arquivo, a resolução do vídeo ou a qualidade do áudio e clique em "Baixar".',
            wraplength=500,
            justify='center',
        ).grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        # ctk.CTkOptionMenu(
        #     self.conteudo,
        #     values=['dark', 'light', 'system'],
        #     width=150,
        #     height=30,
        #     command=self.change_theme,
        # ).grid(row=3, column=1, padx=10, pady=10, sticky='w')

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)

    def esconder_menu_res_video(self, valor):
        if valor == 'mp3':
            self.res_video.configure(state='disabled')
        else:
            self.res_video.configure(state='normal')

        if valor == 'mp4':
            self.config_audio.configure(state='disabled')
        else:
            self.config_audio.configure(state='normal')

    def abrir_segunda_janela(self):
        # Validar URL
        url = self.url_video.get().strip()
        if not url:
            messagebox.showerror(
                'Erro',
                'Por favor, digite uma URL do YouTube válida.',
            )
            return

        # Obter configurações selecionadas
        file_type = self.formato_arquivo.get()
        resolution = self.res_video.get() if file_type == 'mp4' else self.config_audio.get()

        # Abrir janela de download
        if self.segunda_janela is None or not self.segunda_janela.winfo_exists():
            self.segunda_janela = DownloadVideo(on_complete_callback=self.on_download_complete)
        else:
            self.segunda_janela.focus()
            return

        # Iniciar download em uma thread separada
        download_thread = threading.Thread(
            target=self.download_video,
            args=(url, resolution, file_type, None),
        )
        download_thread.daemon = True
        download_thread.start()

    def on_download_complete(self):
        """Callback chamado quando o download é concluído com sucesso"""
        self.url_video.delete(0, 'end')

    def download_video(self, url, resolution=None, file_type='mp4', output_path=None):
        try:
            self.segunda_janela.update_status('Conectando ao YouTube...')
            yt = YouTube(url, 'WEB')
            self.segunda_janela.update_status(f'Obtendo streams para: {yt.title[:40]}...')

            if file_type == 'mp4':
                streams = yt.streams.filter(progressive=True, file_extension='mp4')
                available_resolutions = get_available_resolutions(streams)
                if resolution and resolution not in available_resolutions:
                    raise Exception(
                        f"Resolução {resolution} não disponível. Resoluções disponíveis: {', '.join(available_resolutions)}")
                elif not resolution:
                    resolution = available_resolutions[-1]
                self.segunda_janela.update_status(f'Baixando vídeo em {resolution}...')
                self.video_stream = streams.filter(res=resolution).first()
            elif file_type == 'mp3':
                streams = yt.streams.filter(only_audio=True, file_extension='mp4')
                available_qualities = get_available_audio_qualities(streams)
                if resolution and resolution not in available_qualities:
                    raise Exception(
                        f"Qualidade de áudio {resolution} não disponível. Qualidades disponíveis: {', '.join(available_qualities)}")
                elif not resolution:
                    resolution = available_qualities[-1]
                self.segunda_janela.update_status(f'Baixando áudio em {resolution}...')
                self.video_stream = streams.filter(abr=resolution).first()

            if not self.video_stream:
                raise Exception(
                    f"Nenhum stream disponível para a combinação escolhida de resolução/qualidade {resolution} e tipo {file_type}.")

            if output_path is None:
                sanitized_title = sanitize_filename(yt.title)
                output_path = sanitized_title + ('.mp4' if file_type == 'mp4' else '.mp3')

            self.segunda_janela.update_status(f'Salvando arquivo: {output_path}')
            download_path = self.video_stream.download(output_path=output_path)

            if file_type == 'mp3':
                audio_output_path = output_path
                self.segunda_janela.update_status('Convertendo para MP3...')
                with AudioFileClip(download_path) as audio:
                    audio.write_audiofile(audio_output_path, verbose=False, logger=None)
                os.remove(download_path)

            self.segunda_janela.download_complete_ui()
            print(f"Download concluído! Arquivo salvo em: {output_path}")
        except Exception as e:
            error_message = str(e)
            print(f"Ocorreu um erro durante o download: {error_message}")
            self.segunda_janela.download_error_ui(error_message)


if __name__ == '__main__':
    app = App()
    app.mainloop()
